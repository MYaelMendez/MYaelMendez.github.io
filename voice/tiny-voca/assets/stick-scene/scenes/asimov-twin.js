// asimov-twin: human feeds a qpos card into the USD twin machine, Asimov walks out and back
(function () {
  const SC = (window.SCENES = window.SCENES || {});
  const R = window.RIG;
  const { C, E, P, mix, legs, walkSeg, fig, rr, inkFill, ln, text, seg, breathe, pulse, arcPt, tickBadge, sparks } = R;
  const AS = '#d97757', AD = '#a8553a', AF = '#e8b7a3';

  const GIRL = '#ff4fd8', GIRL_DARK = '#a81586', HERMES = '#00ccff', HERMES_DARK = '#006f91';
  function nousFront(g, J) {
    g.save(); g.lineJoin = 'round';
    g.fillStyle = 'rgba(255,79,216,.18)'; g.strokeStyle = GIRL; g.lineWidth = 1.7;
    g.beginPath();
    g.moveTo(J.sh[0]-9, J.sh[1]-5); g.lineTo(J.sh[0]+9, J.sh[1]-5);
    g.lineTo(J.hip[0]+8, J.hip[1]+3); g.lineTo(J.hip[0]-8, J.hip[1]+3);
    g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(J.hip[0]-5, J.hip[1]-8); g.lineTo(J.hip[0]+5, J.hip[1]-8); g.stroke();
    g.beginPath();
    g.moveTo(J.hip[0]-8, J.hip[1]+2); g.lineTo(J.hip[0]+8, J.hip[1]+2);
    g.lineTo(J.hip[0]+12, J.hip[1]+13); g.lineTo(J.hip[0]-12, J.hip[1]+13);
    g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.arc(J.hc[0], J.hc[1]-1, 15, Math.PI*0.92, Math.PI*2.08); g.stroke();
    g.strokeStyle = GIRL_DARK; g.lineWidth = 2.4;
    g.beginPath();
    g.moveTo(J.hc[0]-11, J.hc[1]-6); g.lineTo(J.hc[0]-15, J.hc[1]+9);
    g.moveTo(J.hc[0]+11, J.hc[1]-6); g.lineTo(J.hc[0]+15, J.hc[1]+9);
    g.stroke();
    g.strokeStyle = GIRL; g.lineWidth = 1.4;
    g.beginPath();
    g.moveTo(J.chest[0]-5, J.chest[1]-2); g.lineTo(J.chest[0]-2, J.chest[1]-2);
    g.lineTo(J.chest[0], J.chest[1]-6); g.lineTo(J.chest[0]+2, J.chest[1]+2);
    g.lineTo(J.chest[0]+5, J.chest[1]+2); g.stroke();
    g.restore();
  }
  function hermesFront(g, J) {
    g.save(); g.lineJoin = 'round';
    g.fillStyle = 'rgba(0,204,255,.15)'; g.strokeStyle = HERMES; g.lineWidth = 1.7;
    g.beginPath();
    g.moveTo(J.hc[0]-13, J.hc[1]-3); g.quadraticCurveTo(J.hc[0], J.hc[1]-22, J.hc[0]+13, J.hc[1]-3);
    g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(J.hc[0]-10, J.hc[1]-2); g.lineTo(J.hc[0]+10, J.hc[1]-2); g.stroke();
    g.beginPath();
    g.moveTo(J.hc[0]+12, J.hc[1]-8); g.quadraticCurveTo(J.hc[0]+25, J.hc[1]-17, J.hc[0]+28, J.hc[1]-6);
    g.quadraticCurveTo(J.hc[0]+20, J.hc[1]-9, J.hc[0]+12, J.hc[1]-2); g.closePath(); g.fill(); g.stroke();
    g.beginPath();
    g.moveTo(J.hc[0]-12, J.hc[1]-8); g.quadraticCurveTo(J.hc[0]-24, J.hc[1]-16, J.hc[0]-27, J.hc[1]-6);
    g.quadraticCurveTo(J.hc[0]-20, J.hc[1]-9, J.hc[0]-12, J.hc[1]-2); g.closePath(); g.fill(); g.stroke();
    g.strokeStyle = HERMES_DARK; g.lineWidth = 1.5;
    const cx = J.chest[0], cy = J.chest[1];
    g.beginPath(); g.moveTo(cx, cy+10); g.lineTo(cx, cy-10); g.stroke();
    g.beginPath();
    g.moveTo(cx-4, cy+6); g.quadraticCurveTo(cx+6, cy+2, cx-4, cy-2);
    g.moveTo(cx+4, cy+6); g.quadraticCurveTo(cx-6, cy+2, cx+4, cy-2);
    g.stroke();
    g.beginPath();
    g.moveTo(cx, cy-9); g.lineTo(cx-6, cy-12); g.moveTo(cx, cy-9); g.lineTo(cx+6, cy-12);
    g.stroke();
    g.restore();
  }
  function asimovFront(g, J) {
    g.save(); g.lineJoin = 'round';
    g.strokeStyle = AD; g.lineWidth = 1.1;
    g.strokeRect(J.hc[0]-14, J.hc[1]-11, 28, 22);
    g.fillStyle = '#141414'; g.fillRect(J.hc[0]-10, J.hc[1]-6, 20, 8);
    g.strokeRect(J.hc[0]-18, J.hc[1]-7, 5, 14);
    g.strokeRect(J.hc[0]+13, J.hc[1]-7, 5, 14);
    g.beginPath(); g.moveTo(J.hc[0], J.hc[1]-11); g.lineTo(J.hc[0], J.hc[1]-20); g.stroke();
    g.fillStyle = '#d4af37'; g.beginPath(); g.arc(J.hc[0], J.hc[1]-22, 2.4, 0, Math.PI*2); g.fill();
    g.fillStyle = 'rgba(217,119,87,.35)';
    g.beginPath();
    g.moveTo(J.sh[0]-9, J.sh[1]-4); g.lineTo(J.sh[0]+9, J.sh[1]-4);
    g.lineTo(J.hip[0]+7, J.hip[1]+3); g.lineTo(J.hip[0]-7, J.hip[1]+3);
    g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(J.chest[0], J.sh[1]-3); g.lineTo(J.chest[0], J.hip[1]+2); g.stroke();
    g.fillStyle = AD;
    [J.sh, J.eF, J.eB, J.kF, J.kB, J.hip].forEach(function (p) {
      g.beginPath(); g.arc(p[0], p[1], 2.6, 0, Math.PI*2); g.fill();
    });
    g.fillRect(J.fF[0]-5, J.fF[1]-2, 10, 3); g.fillRect(J.fB[0]-5, J.fB[1]-2, 10, 3);
    g.restore();
  }

  const ME = -150, START = 62, OUT = 158;
  const M = { x: -120, y: -150, w: 128, h: 104 };
  const RAIL = [-20, 178];

  function machine(g, k, tick) {
    R.stand(g, M.x + 20, M.x + M.w - 20, M.y + M.h);
    rr(g, M.x, M.y, M.w, M.h, 5);
    inkFill(g, C.paper, 1.7);
    text(g, 'asimov-avatar.usda', M.x + M.w / 2, M.y + 16, 8.5, C.ink);
    ['26 links', '25 joints', '216 qpos frames'].forEach((s, i) => text(g, s, M.x + 14, M.y + 40 + i * 14, 8, C.muted, 'left'));
    ln(g, M.x + 14, M.y + 84, M.x + 14 + 100 * k, M.y + 84, 3, '#1a7f37');
    if (tick > 0) tickBadge(g, M.x + M.w - 12, M.y + 30, tick, 8, '#e6f4ea', '#1a7f37');
  }

  function rail(g) {
    ln(g, RAIL[0], -10, RAIL[1], -10, 2.2, C.ink);
    for (let x = RAIL[0]; x <= RAIL[1]; x += 22) ln(g, x, -10, x, -13, 1.2, C.muted);
  }

  SC['asimov-twin'] = {
    dur: 7,
    width: 420,
    label: 'A human feeds a qpos card into the Asimov USD twin and the robot walks out onto the stage.',
    draw(g, S) {
      const U = S.on ? S.u * this.dur : -1;
      const t = S.t;
      let pose = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t);
      let cardK = 0, tick = 0, glow = 0, happy = 0, botX = START, bg = { ph: 0, amp: 0, stride: 0 };
      if (U < 0) {
        pose = mix(pose, P({ hF: [10, -96], head: [7, -116], hB: [-4, -54] }), pulse(t, 5.7, 2.2, 2));
      } else {
        const fade = 1 - seg(U, this.dur - 0.45, this.dur);
        cardK = seg(U, 0.7, 1.7) * (1 - seg(U, 2.0, 2.4)) * fade;
        glow = E.soft(seg(U, 1.8, 2.4)) * (1 - E.soft(seg(U, 4.7, 5.0))) * fade;
        if (U < 2.5) { botX = START; }
        else if (U < 4.0) { const out = walkSeg(U, 2.5, 4.0, START, OUT); botX = out.x; bg = out; }
        else if (U < 5.0) { botX = OUT; }
        else { const back = walkSeg(U, 5.0, 6.3, OUT, START); botX = back.x; bg = { ph: -back.ph, amp: back.amp, stride: back.stride }; }
        tick = seg(U, 4.0, 4.4) * fade;
        happy = E.back(seg(U, 4.4, 4.7)) * (1 - seg(U, 5.5, 5.9)) * fade;
      }
      rail(g);
      machine(g, Math.max(cardK, tick), tick);
      if (cardK > 0 && cardK < 1) {
        const p = arcPt([ME + 18, -96], [M.x + M.w / 2, -104], 44, E.soft(cardK));
        g.save();
        g.translate(p[0], p[1]);
        rr(g, -18, -9, 36, 18, 2);
        inkFill(g, C.butter, 1.3);
        text(g, 'qpos', 0, 3, 8, C.ink);
        g.restore();
      }
      fig(g, pose, ME, 0, { wave: S.wave, wt: S.wt, front: nousFront });
      text(g, 'nous girl', ME, 16, 8.5, GIRL);
      const bp = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t + 1);
      const bgPose = legs(bp, bg.ph, bg.amp, { arms: false, stride: bg.stride });
      fig(g, bgPose, botX, 0, { ink: AS, far: AF, bot: { col: AS, dark: AD, glow, happy: happy > 0.5, blink: pulse(t, 4.3, 1.2, 0.15) > 0.5 }, front: asimovFront });
      text(g, 'asimov', botX, 16, 9, AS);
      if (happy > 0.1) sparks(g, botX, -120, happy, 13, 5, AS);
      R.bubble(g, -20, -132, 'twin synced', tick, { tail: 12 });
    },
  };
})();
