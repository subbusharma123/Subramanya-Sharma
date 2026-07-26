// ===== 3D PORTFOLIO EFFECTS =====

// Initialize Three.js background
let scene, camera, renderer;

function init3DBackground() {
  const canvas = document.getElementById('canvas-bg');
  if (!canvas) return;

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setClearColor(0x000000, 0);

  camera.position.z = 5;

  // Create floating geometric objects
  const geometry = new THREE.IcosahedronGeometry(1, 4);
  const material = new THREE.MeshPhongMaterial({
    color: 0x00d9ff,
    emissive: 0x00d9ff,
    emissiveIntensity: 0.2,
    wireframe: false,
  });

  const mesh1 = new THREE.Mesh(geometry, material.clone());
  mesh1.position.set(-3, 2, -2);
  mesh1.scale.set(0.5, 0.5, 0.5);
  scene.add(mesh1);

  const mesh2 = new THREE.Mesh(geometry, material.clone());
  mesh2.position.set(3, -1, -1);
  mesh2.scale.set(0.7, 0.7, 0.7);
  mesh2.material.color.setHex(0x8338ec);
  mesh2.material.emissive.setHex(0x8338ec);
  scene.add(mesh2);

  const mesh3 = new THREE.Mesh(geometry, material.clone());
  mesh3.position.set(0, 0, -3);
  mesh3.scale.set(0.6, 0.6, 0.6);
  mesh3.material.color.setHex(0xff006e);
  mesh3.material.emissive.setHex(0xff006e);
  scene.add(mesh3);

  // Add lighting
  const light1 = new THREE.PointLight(0x00d9ff, 1, 100);
  light1.position.set(5, 5, 5);
  scene.add(light1);

  const light2 = new THREE.PointLight(0x8338ec, 1, 100);
  light2.position.set(-5, -5, 5);
  scene.add(light2);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
  scene.add(ambientLight);

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);

    mesh1.rotation.x += 0.001;
    mesh1.rotation.y += 0.002;
    mesh1.position.z += Math.sin(Date.now() * 0.0001) * 0.01;

    mesh2.rotation.x -= 0.002;
    mesh2.rotation.y -= 0.001;
    mesh2.position.z += Math.cos(Date.now() * 0.00012) * 0.01;

    mesh3.rotation.x += 0.0015;
    mesh3.rotation.y += 0.0015;
    mesh3.position.z += Math.sin(Date.now() * 0.00008) * 0.01;

    renderer.render(scene, camera);
  }

  animate();

  // Handle resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}

// ===== PARALLAX SCROLL EFFECT =====
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  
  if (scene && camera) {
    camera.position.z = 5 + scrolled * 0.001;
  }

  // Parallax background elements
  const parallaxElements = document.querySelectorAll('.parallax-bg');
  parallaxElements.forEach(el => {
    el.style.transform = `translateY(${scrolled * 0.5}px)`;
  });

  // 3D cards tilt effect
  const cards = document.querySelectorAll('.project-card-3d');
  cards.forEach(card => {
    const rect = card.getBoundingClientRect();
    const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
    
    if (isVisible) {
      const progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      const rotation = (progress - 0.5) * 10;
      card.style.transform = `rotateX(${rotation * 0.5}deg) rotateZ(${rotation}deg)`;
    }
  });
});

// ===== MOUSE FOLLOW FOR SKILL TILES =====
document.addEventListener('mousemove', (e) => {
  const tiles = document.querySelectorAll('.skill-tile');
  tiles.forEach(tile => {
    const rect = tile.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    tile.style.setProperty('--mouse-x', `${x}px`);
    tile.style.setProperty('--mouse-y', `${y}px`);
  });
});

// ===== SCROLL REVEAL ANIMATION =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animation = 'slideInLeft 0.8s ease-out forwards';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.project-card-3d, .skill-tile').forEach(el => {
  observer.observe(el);
});

// ===== ROUTER & SPA LOGIC =====
const main = document.getElementById('spa-root');

const routes = {
  '/': 'home',
  '/experience': 'experience',
  '/projects': 'projects',
  '/skills': 'skills',
  '/certifications': 'certifications'
};

async function navigate(url) {
  try {
    const response = await fetch(url);
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const newContent = doc.querySelector('main').innerHTML;
    main.innerHTML = newContent;
    window.history.pushState(null, '', url);
    window.scrollTo(0, 0);
    init3DBackground();
  } catch (err) {
    console.error('Navigation failed:', err);
  }
}

document.addEventListener('click', (e) => {
  if (e.target.closest('[data-link]')) {
    e.preventDefault();
    const href = e.target.closest('[data-link]').getAttribute('href');
    navigate(href);
  }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  init3DBackground();
  createFloatingParticles();
});

// ===== FLOATING PARTICLES =====
function createFloatingParticles() {
  const particlesContainer = document.querySelector('.particles');
  if (!particlesContainer) return;

  for (let i = 0; i < 30; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDuration = (Math.random() * 20 + 10) + 's';
    particle.style.animationDelay = Math.random() * 5 + 's';
    particlesContainer.appendChild(particle);
  }
}

// ===== MODAL LOGIC =====
function openModal(title, content) {
  const modal = document.getElementById('skillModal');
  if (modal) {
    const titleEl = document.querySelector('.modal-title');
    const descEl = document.querySelector('.modal-desc');
    if (titleEl) titleEl.textContent = title;
    if (descEl) descEl.textContent = content;
    modal.classList.add('active');
  }
}

function closeModal() {
  const modal = document.getElementById('skillModal');
  if (modal) {
    modal.classList.remove('active');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const closeBtn = document.getElementById('closeModal');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  const modal = document.getElementById('skillModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }
});

// ===== CONTACT FLOAT BUTTON =====
const contactBtn = document.getElementById('contact-float');
if (contactBtn) {
  contactBtn.addEventListener('click', () => {
    const modal = document.getElementById('contact-modal');
    if (modal) {
      modal.classList.add('active');
    }
  });
}

// Theme toggle
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}

// Initialize theme
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
