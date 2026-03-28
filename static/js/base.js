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
document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById("page-overlay");

    setTimeout(() => {
        overlay.classList.add("is-revealed");
    }, 50);

    const links = document.querySelectorAll('a[href]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetUrl = this.getAttribute('href');

            if (this.target === '_blank' || targetUrl.startsWith('#') || targetUrl === '' || e.ctrlKey || e.metaKey) {
                return;
            }

            e.preventDefault();

            overlay.classList.remove("is-revealed");
            overlay.classList.add("is-covering-prep");

            void overlay.offsetWidth;

            overlay.classList.remove("is-covering-prep");
            overlay.classList.add("is-covering-active");

            setTimeout(() => {
                window.location.href = this.href;
            }, 320);
        });
    });
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