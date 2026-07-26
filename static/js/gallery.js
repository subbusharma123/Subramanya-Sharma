
// ── THEME TOGGLE ─────────────────────────────────────────────
function initTheme() {
  var saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}
function toggleTheme() {
  var cur = document.documentElement.getAttribute('data-theme');
  var next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcon(next);
  if (window.__threeRenderer) window.__threeRenderer.setClearColor(next === 'light' ? 0xdde8f5 : 0x050510, 1);
}
function updateThemeIcon(theme) {
  var btn = document.getElementById('theme-btn');
  if (btn) btn.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}
document.addEventListener('DOMContentLoaded', function() {
  initTheme();

  // Scroll hint: on home page navigate to /portfolio; elsewhere scroll down
  var hint = document.querySelector('.scroll-hint');
  if (hint) {
    hint.style.cursor = 'pointer';
    hint.addEventListener('click', function() {
      var target = document.querySelector('.page-section');
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.location.href = '/portfolio';
      }
    });
  }
});

// ── THREE.JS BACKGROUND ──────────────────────────────────────
(function() {
  if (typeof THREE === 'undefined') return;
  var scene  = new THREE.Scene();
  var W = window.innerWidth, H = window.innerHeight;
  var camera = new THREE.PerspectiveCamera(75, W/H, 0.1, 1000);
  camera.position.z = 30;
  var renderer = new THREE.WebGLRenderer({canvas:document.getElementById('three-canvas'), antialias:true, alpha:true});
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  var isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  renderer.setClearColor(isDark ? 0x050510 : 0xdde8f5, 1);
  window.__threeRenderer = renderer;

  var sGeo = new THREE.BufferGeometry();
  var sPos = new Float32Array(4000 * 3);
  for (var i = 0; i < sPos.length; i++) sPos[i] = (Math.random() - 0.5) * 500;
  sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
  var stars = new THREE.Points(sGeo, new THREE.PointsMaterial({color:0xaaaacc, size:.2, transparent:true, opacity:.7}));
  scene.add(stars);

  function cloud(n, col, sp, sz) {
    var g = new THREE.BufferGeometry();
    var p = new Float32Array(n * 3);
    for (var i = 0; i < n * 3; i++) p[i] = (Math.random() - 0.5) * sp;
    g.setAttribute('position', new THREE.BufferAttribute(p, 3));
    scene.add(new THREE.Points(g, new THREE.PointsMaterial({color:col, size:sz, transparent:true, opacity:.3})));
  }
  cloud(500, 0x667eea, 140, .55);
  cloud(350, 0xa855f7, 110, .45);
  cloud(250, 0xf0abfc,  90, .35);

  var shapes = [];
  var geoList = [
    new THREE.IcosahedronGeometry(2.2, 0), new THREE.OctahedronGeometry(1.7, 0),
    new THREE.TetrahedronGeometry(2.0, 0), new THREE.IcosahedronGeometry(1.4, 0),
    new THREE.OctahedronGeometry(2.4, 0),  new THREE.IcosahedronGeometry(1.1, 0),
  ];
  var cols = [0x667eea, 0xa855f7, 0xf0abfc, 0x4facfe, 0xfa709a, 0x43e97b];
  geoList.forEach(function(g, i) {
    var m = new THREE.Mesh(g, new THREE.MeshPhongMaterial({color:cols[i], wireframe:true, transparent:true, opacity:.18}));
    m.position.set((Math.random()-.5)*70, (Math.random()-.5)*45, (Math.random()-.5)*35);
    m.rotation.set(Math.random()*Math.PI, Math.random()*Math.PI, 0);
    scene.add(m);
    shapes.push({m:m, rx:(Math.random()-.5)*.007, ry:(Math.random()-.5)*.007, fo:Math.random()*Math.PI*2, fs:Math.random()*.0005+.0003});
  });

  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  var pl  = new THREE.PointLight(0x667eea, 2,   120); pl.position.set(20, 20, 20);  scene.add(pl);
  var pl2 = new THREE.PointLight(0xa855f7, 1.5, 100); pl2.position.set(-20,-10,10); scene.add(pl2);

  var mouse = {x:0, y:0}, tMouse = {x:0, y:0};
  document.addEventListener('mousemove', function(e) {
    // Negate so camera moves opposite → scene follows mouse
    tMouse.x = -(e.clientX / window.innerWidth  - 0.5) * 0.6;
    tMouse.y =  (e.clientY / window.innerHeight - 0.5) * 0.4;
  });

  var clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    var t = clock.getElapsedTime();
    mouse.x += (tMouse.x - mouse.x) * 0.04;
    mouse.y += (tMouse.y - mouse.y) * 0.04;
    camera.position.x = mouse.x * 10;
    camera.position.y = mouse.y * 7;
    camera.lookAt(0, 0, 0);
    shapes.forEach(function(s) {
      s.m.rotation.x += s.rx; s.m.rotation.y += s.ry;
      s.m.position.y += Math.sin(t * s.fs * 60 + s.fo) * 0.009;
    });
    stars.rotation.y = t * 0.01;
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();
