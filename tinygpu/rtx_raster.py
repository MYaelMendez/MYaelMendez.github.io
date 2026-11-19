"""RTX rasteriser — CAD triangles rendered on CUDA, no OpenGL ICD needed.

Why this exists: the Optimus laptop has no registered NVIDIA OpenGL ICD, so
MuJoCo's GL path lands on Intel UHD. CUDA is unaffected. So rasterise on the
RTX ourselves: MuJoCo supplies physics and body transforms (cheap, CPU), the
GPU projects and z-buffers every triangle.

Correctness note: a depth atomicMin followed by a separate colour write is a
RACE — two fragments can both pass and write out of order. Pack depth into the
high 32 bits and triangle id into the low 32 of a uint64 and atomicMin that,
then shade in a second pass from the winning id. Race-free.
"""
from __future__ import annotations

import os
import struct
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = Path(os.environ.get('ASIMOV_MODEL', HERE / 'model'))
PL = MODEL.parent
OUT = Path(os.environ.get('ASIMOV_OUT', HERE / 'out'))

DEPTH = r'''
extern "C" __global__ void depth_pass(
    const float* verts, const float* mvp,
    unsigned long long* zid,          // (H,W) packed depth<<32 | (tri+1)
    const int T, const int W, const int H)
{
    int t = blockIdx.x * blockDim.x + threadIdx.x;
    if (t >= T) return;
    float2 p[3]; float pz[3];
    for (int i = 0; i < 3; ++i) {
        float x = verts[t*9+i*3+0], y = verts[t*9+i*3+1], z = verts[t*9+i*3+2];
        float cx = mvp[0]*x+mvp[1]*y+mvp[2]*z+mvp[3];
        float cy = mvp[4]*x+mvp[5]*y+mvp[6]*z+mvp[7];
        float cz = mvp[8]*x+mvp[9]*y+mvp[10]*z+mvp[11];
        float cw = mvp[12]*x+mvp[13]*y+mvp[14]*z+mvp[15];
        if (cw <= 1e-6f) return;
        p[i] = make_float2((cx/cw*0.5f+0.5f)*W, (1.0f-(cy/cw*0.5f+0.5f))*H);
        pz[i] = cz/cw;
        if (pz[i] < 0.0f || pz[i] > 1.0f) return;
    }
    float minx=fminf(fminf(p[0].x,p[1].x),p[2].x), maxx=fmaxf(fmaxf(p[0].x,p[1].x),p[2].x);
    float miny=fminf(fminf(p[0].y,p[1].y),p[2].y), maxy=fmaxf(fmaxf(p[0].y,p[1].y),p[2].y);
    int x0=max(0,(int)floorf(minx)), x1=min(W-1,(int)ceilf(maxx));
    int y0=max(0,(int)floorf(miny)), y1=min(H-1,(int)ceilf(maxy));
    if (x1<x0 || y1<y0) return;
    float area=(p[1].x-p[0].x)*(p[2].y-p[0].y)-(p[2].x-p[0].x)*(p[1].y-p[0].y);
    if (fabsf(area)<1e-9f) return;
    float inv=1.0f/area;
    for (int y=y0; y<=y1; ++y) for (int x=x0; x<=x1; ++x) {
        float px=x+0.5f, py=y+0.5f;
        float w0=((p[1].x-px)*(p[2].y-py)-(p[2].x-px)*(p[1].y-py))*inv;
        float w1=((p[2].x-px)*(p[0].y-py)-(p[0].x-px)*(p[2].y-py))*inv;
        float w2=1.0f-w0-w1;
        if (w0<0||w1<0||w2<0) continue;
        float z=w0*pz[0]+w1*pz[1]+w2*pz[2];
        unsigned int zi=__float_as_uint(z);   // positive floats order as uints
        unsigned long long packed=((unsigned long long)zi<<32)|(unsigned long long)(t+1);
        atomicMin(&zid[y*W+x], packed);
    }
}
'''

SHADE = r'''
extern "C" __global__ void shade_pass(
    const unsigned long long* zid, const float* norms, const float* cols,
    unsigned char* img, const int W, const int H,
    const float bg_r, const float bg_g, const float bg_b)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= W*H) return;
    unsigned long long v = zid[i];
    unsigned int t = (unsigned int)(v & 0xFFFFFFFFULL);
    if (t == 0) {
        // void gradient, not flat black — the gate needs luminance
        float gy = (float)(i / W) / (float)H;
        img[i*3+0]=(unsigned char)(bg_r*(0.35f+0.65f*gy)*255);
        img[i*3+1]=(unsigned char)(bg_g*(0.35f+0.65f*gy)*255);
        img[i*3+2]=(unsigned char)(bg_b*(0.35f+0.65f*gy)*255);
        return;
    }
    t -= 1;
    float nx=norms[t*3+0], ny=norms[t*3+1], nz=norms[t*3+2];
    float key=fmaxf(0.0f, nx*0.40f + ny*(-0.55f) + nz*0.73f);
    float fill=fmaxf(0.0f, nx*(-0.6f) + ny*0.2f + nz*0.3f)*0.35f;
    float shade=0.22f + 0.78f*key + fill;
    img[i*3+0]=(unsigned char)(fminf(1.0f,cols[t*3+0]*shade)*255);
    img[i*3+1]=(unsigned char)(fminf(1.0f,cols[t*3+1]*shade)*255);
    img[i*3+2]=(unsigned char)(fminf(1.0f,cols[t*3+2]*shade)*255);
}
'''


def load_stl(p):
    b = p.read_bytes()
    n = struct.unpack('<I', b[80:84])[0]
    if len(b) < 84 + n * 50:
        raise ValueError(f'{p.name}: truncated')
    raw = np.frombuffer(b, dtype=np.uint8, count=n * 50, offset=84).reshape(n, 50)
    rec = raw[:, :48].copy().view('<f4').reshape(n, 12)
    tri = rec.reshape(n, 4, 3)
    v = tri[:, 1:, :].astype(np.float32)
    nrm = tri[:, 0, :].astype(np.float32)
    ln = np.linalg.norm(nrm, axis=1, keepdims=True)
    nrm = np.divide(nrm, ln, out=np.zeros_like(nrm), where=ln > 1e-9)
    return v, nrm


def persp(fov_deg, near, far, aspect=1.0):
    f = 1.0 / np.tan(np.radians(fov_deg) / 2)
    A = far / (far - near)
    B = -near * far / (far - near)
    return np.array([[f / aspect, 0, 0, 0], [0, f, 0, 0],
                     [0, 0, A, B], [0, 0, 1, 0]], dtype=np.float32)


def look_at(eye, target, up=(0, 0, 1)):
    eye = np.asarray(eye, np.float32); target = np.asarray(target, np.float32)
    fwd = target - eye; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, np.asarray(up, np.float32)); right /= np.linalg.norm(right)
    u = np.cross(right, fwd)
    # world -> camera: camera looks down +Z
    R = np.stack([right, u, fwd], axis=0)
    M = np.eye(4, dtype=np.float32)
    M[:3, :3] = R
    M[:3, 3] = -R @ eye
    return M


class RtxRenderer:
    def __init__(self, w, h):
        import cupy as cp
        self.cp = cp
        self.w, self.h = w, h
        self.kd = cp.RawKernel(DEPTH, 'depth_pass')
        self.ks = cp.RawKernel(SHADE, 'shade_pass')
        self.zid = cp.zeros((h, w), dtype=cp.uint64)
        self.img = cp.zeros((h, w, 3), dtype=cp.uint8)
        self.px = cp.RawKernel  # placeholder to keep cp referenced

    def render(self, verts, norms, cols, mvp, bg=(0.02, 0.03, 0.05)):
        cp = self.cp
        T = len(verts)
        gv = cp.asarray(verts.ravel(), dtype=cp.float32)
        gn = cp.asarray(norms.ravel(), dtype=cp.float32)
        gc = cp.asarray(cols.ravel(), dtype=cp.float32)
        gm = cp.asarray(mvp.ravel(), dtype=cp.float32)
        # depth = max, id = 0. All-ones would make the low bits read as
        # triangle 0xFFFFFFFF and index far past the colour buffer.
        self.zid.fill(cp.uint64(0xFFFFFFFF00000000))
        th = 128
        self.kd(((T + th - 1) // th,), (th,), (gv, gm, self.zid, T, self.w, self.h))
        n = self.w * self.h
        self.ks(((n + th - 1) // th,), (th,),
                (self.zid, gn, gc, self.img, self.w, self.h,
                 cp.float32(bg[0]), cp.float32(bg[1]), cp.float32(bg[2])))
        cp.cuda.Stream.null.synchronize()
        return cp.asnumpy(self.img)


def main():
    import cupy as cp
    OUT.mkdir(parents=True, exist_ok=True)
    print(f'  device: {cp.cuda.runtime.getDeviceProperties(0)["name"].decode()}')
    meshes = sorted((MODEL / 'meshes').glob('*.STL'))
    v, n = load_stl(meshes[0])
    print(f'  mesh: {meshes[0].name}  {len(v)} triangles')

    # centre and fit the part, camera orbiting it
    ctr = v.reshape(-1, 3).mean(axis=0)
    rad = float(np.linalg.norm(v.reshape(-1, 3) - ctr, axis=1).max())
    v = v - ctr
    cols = np.tile(np.array([0.83, 0.69, 0.22], np.float32), (len(v), 1))

    W, Hh = 720, 720
    r = RtxRenderer(W, Hh)
    P = persp(45, 0.05, rad * 8)
    eye = np.array([rad * 2.6, -rad * 2.6, rad * 1.4], np.float32)
    M = P @ look_at(eye, [0, 0, 0])

    r.render(v, n, cols, M)                      # warmup
    t0 = time.time()
    N = 20
    for _ in range(N):
        img = r.render(v, n, cols, M)
    dt = (time.time() - t0) / N
    print(f'  {dt*1000:.2f} ms/frame  ({1/dt:.1f} fps)  {len(v)} tris @ {W}x{Hh}')
    from PIL import Image
    Image.fromarray(img).save(OUT / 'probe2.png')
    print(f'  {OUT/"probe2.png"}')


if __name__ == '__main__':
    main()
