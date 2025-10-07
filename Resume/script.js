// Nav links (page navigation)
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            window.location.href = href;
        }
    });
});

// Toggle for sections
function toggleContent(header) {
    const content = header.nextElementSibling;
    content.classList.toggle('active');
}

// Home filter
if (document.getElementById('highlight-filter')) {
    document.getElementById('highlight-filter').addEventListener('change', function () {
        const val = this.value;
        document.querySelectorAll('.highlight-section').forEach(sec => {
            if (val === 'all' || val === sec.id) {
                sec.classList.remove('hidden');
                setTimeout(() => sec.classList.add('visible'), 10);
            } else {
                sec.classList.remove('visible');
                setTimeout(() => sec.classList.add('hidden'), 500);
            }
        });
    });
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.highlight-section, .content').forEach(el => el.classList.add('visible'));
});

// Home filter (now toggles card containers)
if (document.getElementById('highlight-filter')) {
    document.getElementById('highlight-filter').addEventListener('change', function () {
        const val = this.value;
        document.querySelectorAll('.highlight-section').forEach(sec => {
            if (val === 'all' || val === sec.id) {
                sec.classList.remove('hidden');
                setTimeout(() => {
                    sec.querySelectorAll('.card').forEach(card => card.classList.add('visible'));
                }, 10);
            } else {
                sec.classList.remove('visible');
                setTimeout(() => {
                    sec.classList.add('hidden');
                    sec.querySelectorAll('.card').forEach(card => card.classList.remove('visible'));
                }, 500);
            }
        });
    });
}

// Init cards visible
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => card.classList.add('visible'));
});