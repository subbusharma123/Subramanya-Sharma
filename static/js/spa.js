// ---------- tiny spa router ----------
const main = document.getElementById('spa-root');

document.addEventListener('click', e => {
  const link = e.target.closest('a[data-link]');
  if (!link) return;
  e.preventDefault();
  navigate(link.href);
});

async function navigate(url){
  main.classList.add('spa-out');
  await delay(300);
  const html = await (await fetch(url)).text();
  const newMain = new DOMParser().parseFromString(html, 'text/html').querySelector('#spa-root').innerHTML;
  main.innerHTML = newMain;
  main.classList.remove('spa-out');
  main.classList.add('spa-in');
  window.history.pushState(null, null, url);
  document.title = new DOMParser().parseFromString(html, 'text/html').title;
}
window.addEventListener('popstate', () => navigate(location.pathname));

function delay(ms){ return new Promise(r => setTimeout(r, ms)); }

// ---------- dark-mode toggle ----------
const html = document.documentElement;
const toggle = document.createElement('i');
toggle.className = 'fa-solid fa-circle-half-stroke theme-toggle';
toggle.style.marginLeft = '1rem'; toggle.style.cursor = 'pointer';
document.querySelector('.navbar').appendChild(toggle);

toggle.addEventListener('click', () => {
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});
(function(){
  const saved = localStorage.getItem('theme');
  if (saved) html.setAttribute('data-theme', saved);
})();

// ---------- mobile nav ----------
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));

/*  NEW  */
document.querySelectorAll('.nav-links a[data-link]').forEach(a =>
  a.addEventListener('click', () => navLinks.classList.remove('active'))
);

// ----- footer year -----
document.getElementById('year').textContent = new Date().getFullYear();

/* ---------- auto dark if OS prefers ---------- */
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.documentElement.setAttribute('data-theme', 'dark');
}