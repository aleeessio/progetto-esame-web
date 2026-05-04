//VEHICLE TYPE DROPDOWN + SLIDESHOW
document.addEventListener("DOMContentLoaded", function () {
    // Dropdown Logic
    const trigger = document.getElementById('custom-select-trigger');
    const optionsList = document.getElementById('custom-options');
    const options = optionsList.querySelectorAll('li');
    const searchLinkBtn = document.getElementById('search-link-btn');

    const baseSearchUrl = "/search?type=";

    trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        optionsList.classList.toggle('open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            const selectedVehicle = option.dataset.value;

            trigger.textContent = option.textContent;
            trigger.style.color = 'var(--font-color)';

            if (searchLinkBtn) {
                searchLinkBtn.href = baseSearchUrl + selectedVehicle;
            }
            optionsList.classList.remove('open');
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

        }, 4000);
    }
});