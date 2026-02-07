// ---------- tiny spa router ----------
const main = document.getElementById('spa-root');

document.addEventListener('click', e => {
  // Toggle Interactive Cards
  if (e.target.closest('.interactive-card')) {
    const card = e.target.closest('.interactive-card');
    // If clicking inside the content (e.g. a link), don't toggle if we strictly want that.
    // But here we want the whole card to toggle.

    // Close others (optional - straightforward is to just toggle current)
    // Remove 'active' from siblings? Let's keep it simple: toggle current.

    card.classList.toggle('active');

    const btn = card.querySelector('.toggle-btn');
    if (btn) {
      if (card.classList.contains('active')) {
        btn.innerHTML = '<i class="fa-solid fa-chevron-down"></i> Hide Details';
      } else {
        btn.innerHTML = '<i class="fa-solid fa-chevron-down"></i> Show Details';
      }
    }
  }

  // Close Modal (X button or outside click)
  const link = e.target.closest('a[data-link]');
  if (!link) return;
  e.preventDefault();
  navigate(link.href);
});

async function navigate(url) {
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

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

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
(function () {
  const saved = localStorage.getItem('theme');
  if (saved) html.setAttribute('data-theme', saved);
})();

// ---------- mobile nav ----------
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));

/*  NEW  */
document.querySelectorAll('.nav-links a[data-link]').forEach(a =>
  a.addEventListener('click', () => navLinks.classList.remove('active'))
);

// ----- footer year -----
document.getElementById('year').textContent = new Date().getFullYear();

