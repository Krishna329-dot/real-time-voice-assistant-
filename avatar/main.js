// ===============================
// CANVAS SETUP
// ===============================
const canvas = document.getElementById("holo");
const ctx = canvas.getContext("2d");

const smokeCanvas = document.getElementById("smoke");
const sctx = smokeCanvas.getContext("2d");

function resize() {
  canvas.width = smokeCanvas.width = innerWidth;
  canvas.height = smokeCanvas.height = innerHeight;
}
resize();
addEventListener("resize", resize);

// ===============================
// MIC AUDIO (AUTO SPEAK DETECT)
// ===============================
let audioLevel = 0;
let smoothLevel = 0;

navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  const audioCtx = new AudioContext();
  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 512;

  const mic = audioCtx.createMediaStreamSource(stream);
  mic.connect(analyser);

  const data = new Uint8Array(analyser.frequencyBinCount);

  function audioLoop() {
    analyser.getByteFrequencyData(data);
    let sum = 0;
    for (let i = 0; i < data.length; i++) sum += data[i];
    audioLevel = sum / data.length / 255;
    requestAnimationFrame(audioLoop);
  }
  audioLoop();
}).catch(() => {
  audioLevel = 0;
});

// ===============================
// SMOKE PARTICLES
// ===============================
const smoke = [];
for (let i = 0; i < 70; i++) {
  smoke.push({
    x: Math.random() * innerWidth,
    y: Math.random() * innerHeight,
    r: 60 + Math.random() * 120,
    a: 0.03 + Math.random() * 0.04,
    vx: -0.15 + Math.random() * 0.3,
    vy: -0.15 + Math.random() * 0.3
  });
}

function drawSmoke() {
  sctx.clearRect(0, 0, smokeCanvas.width, smokeCanvas.height);
  smoke.forEach(p => {
    const g = sctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
    g.addColorStop(0, `rgba(0,180,255,${p.a})`);
    g.addColorStop(1, "rgba(0,0,0,0)");
    sctx.fillStyle = g;
    sctx.beginPath();
    sctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    sctx.fill();

    p.x += p.vx;
    p.y += p.vy;
    if (p.x < -p.r) p.x = innerWidth + p.r;
    if (p.y < -p.r) p.y = innerHeight + p.r;
  });
}

// ===============================
// HUD RINGS
// ===============================
let t = 0;

function ring(radius, width, speed, glow) {
  ctx.save();
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate(t * speed);
  ctx.strokeStyle = `rgba(0,220,255,${glow})`;
  ctx.lineWidth = width;
  ctx.shadowColor = "rgba(0,220,255,0.6)";
  ctx.shadowBlur = 20;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

// ===============================
// ANIMATION LOOP
// ===============================
function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawSmoke();

  smoothLevel += (audioLevel - smoothLevel) * 0.1;

  const pulse = smoothLevel * 60;
  const glow = 0.4 + smoothLevel * 0.6;

  ring(120 + pulse, 2 + smoothLevel * 3, 0.4, glow);
  ring(165 + pulse * 0.6, 3 + smoothLevel * 3, -0.6, glow);

  t += 0.01 + smoothLevel * 0.08;
}

animate();
