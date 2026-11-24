// asimov-authority: human types the command, approves it, Asimov acts, receipt prints
(function () {
  const SC = (window.SCENES = window.SCENES || {});
  const R = window.RIG;
  const { C, E, P, mix, legs, walkSeg, fig, rr, inkFill, ln, text, seg, breathe, pulse, lp, tickBadge, bubble, plane, sparks, pill, typed, circle } = R;
  const AS = '#d97757', AD = '#a8553a', AF = '#e8b7a3';
  const HOME = -170, AT = -80, BOT = 156;
  const T = { x: -60, y: -150, w: 140, h: 88 };
  const CMD = '>_æ://asimov_robot';

  function machine(g, cmdK, okK) {
    R.term(g, T.x, T.y, T.w, T.h, 'commandprompt.ai');
    text(g, typed(CMD, cmdK), T.x + 10, T.y + 40, 8.5, '#f5d77a', 'left');
    R.words(g, T.x + 10, T.y + 58, 92, 7, '#6b6b6b', 1.8);
    text(g, 'privateclient.ai', T.x + T.w - 8, T.y + 74, 7.5, '#8fd19e', 'right');
    if (okK > 0) tickBadge(g, T.x + T.w - 10, T.y + 24, okK, 8, '#e6f4ea', '#1a7f37');
  }

  SC['asimov-authority'] = {
    dur: 7,
    width: 420,
    label: 'A human types a command to Asimov, approves it privately, the robot steps forward, and a receipt is printed.',
    draw(g, S) {
      const U = S.on ? S.u * this.dur : -1;
      const t = S.t;
      let x = HOME, hg = { ph: 0, amp: 0, stride: 0 };
      let pose = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t);
      let cmdK = 0, approveK = 0, moveK = 0, receiptK = 0, glow = 0, happy = 0;
      let botX = BOT, bg = { ph: 0, amp: 0, stride: 0 };
      if (U < 0) {
        pose = mix(pose, P({ hF: [10, -96], head: [7, -116], hB: [-4, -54] }), pulse(t, 5.5, 2.4, 2));
      } else {
        const fade = 1 - seg(U, this.dur - 0.45, this.dur);
        const walk = walkSeg(U, 0.15, 0.85, HOME, AT);
        x = walk.x;
        hg = walk;
        if (U >= 5.4) {
          const back = walkSeg(U, 5.4, 6.4, AT, HOME);
          x = back.x;
          hg = { ph: -back.ph, amp: back.amp, stride: back.stride };
        }
        cmdK = seg(U, 0.9, 1.8) * fade;
        approveK = E.back(seg(U, 2.1, 2.5)) * (1 - seg(U, 4.6, 5.0)) * fade;
        const typing = E.soft(seg(U, 0.85, 1.1)) * (1 - E.soft(seg(U, 1.7, 2.0)));
        const keyY = T.y + 42;
        pose = mix(pose, P({ hF: lp([T.x + 12, keyY], x, 0, 1), hB: lp([T.x + 4, keyY + 8], x, 0, 1), head: [7, -114], chest: [4, -89] }), typing);
        pose = mix(pose, P({ hF: lp([T.x + 14, T.y + 72], x, 0, 1), hB: [-4, -54], head: [9, -115] }), E.soft(seg(U, 2.1, 2.4)) * (1 - E.soft(seg(U, 2.5, 2.8))) * fade);
        if (U >= 3 && U < 4) {
          const out = walkSeg(U, 3.0, 4.0, BOT, 104);
          botX = out.x; bg = out;
        } else if (U >= 4 && U < 5.2) {
          botX = 104;
        } else if (U >= 5.2) {
          const back = walkSeg(U, 5.2, 6.3, 104, BOT);
          botX = back.x; bg = { ph: -back.ph, amp: back.amp, stride: back.stride };
        }
        glow = E.soft(seg(U, 2.5, 3.0)) * (1 - E.soft(seg(U, 4.7, 5.0))) * fade;
        moveK = seg(U, 3.1, 3.5) * (1 - seg(U, 3.9, 4.2)) * fade;
        receiptK = seg(U, 4.2, 4.6) * fade;
        happy = E.back(seg(U, 4.5, 4.8)) * (1 - seg(U, 5.5, 5.9)) * fade;
      }
      pose = legs(pose, hg.ph, hg.amp, { arms: false, stride: hg.stride });
      machine(g, cmdK, receiptK);
      if (approveK > 0) pill(g, T.x + 14, -70, 'approve', C.butter, C.ink, 8.5);
      plane(g, [T.x + T.w - 12, -104], [botX - 18, -104], moveK, 46, 0.85);
      plane(g, [botX - 18, -86], [T.x + T.w - 16, -72], receiptK, 40, 0.8);
      fig(g, pose, x, 0, { wave: S.wave, wt: S.wt });
      text(g, 'you', x, 16, 9, C.muted);
      const bp = breathe(P({ hF: [12, -60], hB: [-4, -52] }), t + 1);
      const bgPose = legs(bp, bg.ph, bg.amp, { arms: false, stride: bg.stride });
      fig(g, bgPose, botX, 0, { sx: -1, ink: AS, far: AF, bot: { col: AS, dark: AD, glow, happy: happy > 0.5, blink: pulse(t, 4.3, 1.2, 0.15) > 0.5 } });
      text(g, 'asimov', botX, 16, 9, AS);
      if (happy > 0.1) sparks(g, botX, -120, happy, 14, 5, AS);
      bubble(g, x + 4, -136, 'approved', approveK * (1 - seg(U, 3.0, 3.3)), { tail: 10 });
    },
  };
})();
