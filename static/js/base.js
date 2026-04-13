//CHANGE THEME
const btnTheme = document.getElementById('theme-toggle');
const sunIcon = document.getElementById('sun-icon');
const moonIcon = document.getElementById('moon-icon');
const body = document.body;

if (localStorage.getItem('theme') === 'dark') {
    sunIcon.style.display = 'none';
    moonIcon.style.display = 'block';
} else {
    sunIcon.style.display = 'block';
    moonIcon.style.display = 'none';
}

btnTheme.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
        localStorage.setItem('theme', 'dark');
    } else {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
        localStorage.setItem('theme', 'light');
    }
});


// PAGE TRANSITION LOGIC
document.addEventListener("DOMContentLoaded", () => {
    window.scrollTo(0, 0);
    const overlay = document.getElementById("page-overlay");

    if (overlay) {
        const isReload = performance.getEntriesByType("navigation")[0]?.type === "reload";

        if (isReload) {
            overlay.style.transition = 'none';
            overlay.classList.add("is-revealed");

            setTimeout(() => {
                overlay.style.transition = '';
            }, 50);
        } else {
            setTimeout(() => {
                overlay.classList.add("is-revealed");
            }, 100);
        }
    }

    const links = document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"])');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            if (!overlay) return;

            const targetBaseUrl = link.href.split('?')[0].split('#')[0];
            const currentBaseUrl = window.location.href.split('?')[0].split('#')[0];

            if (targetBaseUrl === currentBaseUrl) {
                return;
            }

            e.preventDefault();

            overlay.style.transition = '';
            overlay.classList.remove("is-revealed");
            overlay.classList.add("is-covering-prep");

            void overlay.offsetWidth; // Forza reflow del browser

            overlay.classList.add("is-covering-active");

            setTimeout(() => {
                window.location.href = link.href;
            }, 320);
        });
    });
});

// 3. FIX TASTO INDIETRO (Bfcache)
window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
        const overlay = document.getElementById("page-overlay");
        if (overlay) {
            overlay.style.transition = 'none';
            overlay.classList.remove("is-covering-prep", "is-covering-active");
            overlay.classList.add("is-revealed");

            void overlay.offsetWidth;

            overlay.style.transition = '';
        }
    }
});

// AUTO-DISMISS FLASH MESSAGES
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash-message');

    flashes.forEach(flash => {
        if (!flash.classList.contains('logout')) {
            setTimeout(() => {
                flash.classList.add('fade-out');

                setTimeout(() => {
                    flash.remove();
                }, 400);
            }, 3000);
        }
    });
});