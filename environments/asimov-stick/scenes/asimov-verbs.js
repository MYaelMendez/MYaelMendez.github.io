// asimov-verbs: human pulls the governed-verbs lever, Asimov balances and steps, both return
(function () {
  const SC = (window.SCENES = window.SCENES || {});
  const R = window.RIG;
  const { C, E, P, mix, legs, walkSeg, fig, rr, inkFill, ln, text, seg, breathe, pulse, lp, tickBadge, sparks, pill, circle } = R;
  const AS = '#d97757', AD = '#a8553a', AF = '#e8b7a3';
  const HOME = -160, AT = -105, BOT = 150, OUT = 96;
  const M = { x: -100, y: -150, w: 110, h: 100 };
  const LEVER = [-72, -80];

  function machine(g, k, tick) {
    R.stand(g, M.x + 18, M.x + M.w - 18, M.y + M.h);
    rr(g, M.x, M.y, M.w, M.h, 5);
    inkFill(g, C.paper, 1.7);
    text(g, 'æ robot verbs', M.x + M.w / 2, M.y + 16, 9, C.ink);
    ['stand', 'damp', 'balance', 'set_velocity', 'set_joints'].forEach((s, i) => {
      text(g, s, M.x + 12, M.y + 38 + i * 12, 7.5, i === 2 && k > 0.4 ? '#1a7f37' : C.muted, 'left');
    });
    const angle = -0.22 + 0.42 * k;
    g.save();
    g.translate(LEVER[0], LEVER[1]);
    g.rotate(angle);
    ln(g, 0, 0, 0, -34, 3.2, C.ink);
    circle(g, 0, -34, 4.5);
    inkFill(g, k > 0.4 ? C.butter : C.paper, 1.5);
    g.restore();
    circle(g, LEVER[0], LEVER[1], 3);
    inkFill(g, C.ink);
    if (tick > 0) tickBadge(g, M.x + M.w - 12, M.y + 30, tick, 8, '#e6f4ea', '#1a7f37');
  }

  SC['asimov-verbs'] = {
    dur: 6.5,
    width: 420,
    label: 'A human pulls the governed verbs lever and Asimov balances, steps forward, and prints a receipt.',
    draw(g, S) {
      const U = S.on ? S.u * this.dur : -1;
      const t = S.t;
      let x = HOME, hg = { ph: 0, amp: 0, stride: 0 }, bg = { ph: 0, amp: 0, stride: 0 };
      let pose = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t);
      let pull = 0, tick = 0, glow = 0, happy = 0, botX = BOT;
      if (U < 0) {
        pose = mix(pose, P({ hF: [10, -96], head: [7, -116], hB: [-4, -54] }), pulse(t, 5.9, 2.1, 2));
      } else {
        const fade = 1 - seg(U, this.dur - 0.45, this.dur);
        if (U < 5.2) {
          const walk = walkSeg(U, 0.2, 0.9, HOME, AT);
          x = walk.x; hg = walk;
        } else {
          const back = walkSeg(U, 5.2, 6.3, AT, HOME);
          x = back.x; hg = { ph: -back.ph, amp: back.amp, stride: back.stride };
        }
        pull = E.soft(seg(U, 1.0, 1.5)) * (1 - E.soft(seg(U, 2.1, 2.5)));
        const reach = E.soft(seg(U, 0.95, 1.25)) * (1 - E.soft(seg(U, 2.2, 2.55)));
        pose = mix(pose, P({ hF: lp(LEVER, x, 0, 1), hB: [-4, -54], head: [8, -115], chest: [4, -89] }), reach * fade);
        if (U < 2.7) { botX = BOT; }
        else if (U < 4.0) { const out = walkSeg(U, 2.7, 4.0, BOT, OUT); botX = out.x; bg = out; }
        else if (U < 5.2) { botX = OUT; }
        else { const back = walkSeg(U, 5.2, 6.3, OUT, BOT); botX = back.x; bg = { ph: -back.ph, amp: back.amp, stride: back.stride }; }
        glow = E.soft(seg(U, 2.5, 2.9)) * (1 - E.soft(seg(U, 4.4, 4.8))) * fade;
        tick = seg(U, 4.0, 4.4) * fade;
        happy = E.back(seg(U, 4.5, 4.8)) * (1 - seg(U, 5.6, 5.9)) * fade;
      }
      pose = legs(pose, hg.ph, hg.amp, { arms: false, stride: hg.stride });
      machine(g, pull, tick);
      fig(g, pose, x, 0, { wave: S.wave, wt: S.wt });
      text(g, 'you', x, 16, 9, C.muted);
      const bp = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t + 1);
      const bgPose = legs(bp, bg.ph, bg.amp, { arms: false, stride: bg.stride });
      fig(g, bgPose, botX, 0, { sx: -1, ink: AS, far: AF, bot: { col: AS, dark: AD, glow, happy: happy > 0.5, blink: pulse(t, 4.3, 1.2, 0.15) > 0.5 } });
      text(g, 'asimov', botX, 16, 9, AS);
      if (happy > 0.1) sparks(g, botX, -120, happy, 13, 5, AS);
      pill(g, 0, -168, 'HUMAN://ROOT → æ → RECEIPT', C.butter, C.ink, 8);
    },
  };
})();
