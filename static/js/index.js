// SELECTOR CARDS LOGIC
const cards = document.querySelectorAll('.selector-card');
const cta = document.getElementById('selector-cta');
const searchBtn = document.getElementById('search-btn');

let selected = null;

cards.forEach(card => {
    card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('selected'));

        card.classList.add('selected');
        selected = card.dataset.type;

        searchBtn.href = `/search?type=${selected}`;

        cta.classList.add('visible');
    });
});

//VEHICLE TYPE DROPDOWN + SLIDESHOW
document.addEventListener("DOMContentLoaded", function () {
    // Dropdown Logic
    const trigger = document.getElementById('custom-select-trigger');
    const optionsList = document.getElementById('custom-options');
    const input = document.getElementById('vehicle-type-input');
    const options = optionsList.querySelectorAll('li');

    trigger.addEventListener('click', () => {
        optionsList.classList.toggle('open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            trigger.textContent = option.textContent;
            input.value = option.dataset.value;
            optionsList.classList.remove('open');
            trigger.style.color = 'var(--font-color)';
        });
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-select-wrapper')) {
            optionsList.classList.remove('open');
        }
    });

    // Slideshow Logic
    const slides = document.querySelectorAll(".hero-slide");
    let currentSlide = 0;

    if (slides.length > 0) {
        setInterval(() => {
            slides[currentSlide].classList.remove("active");

            currentSlide = (currentSlide + 1) % slides.length;

            slides[currentSlide].classList.add("active");

        }, 6000);
    }
});