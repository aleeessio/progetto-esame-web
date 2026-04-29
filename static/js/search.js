// Favorite toggle logic for search results
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.btn-favorite-search').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const vType = this.getAttribute('data-type');
            const vId = this.getAttribute('data-id');

            fetch(`/toggle_favorite/${vType}/${vId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "redirect") {
                        window.location.href = data.url;
                    }
                    else if (data.status === "added" || data.status === "removed") {
                        this.classList.toggle("is-saved");
                    }
                })
                .catch(err => console.error(err));
        });
    });
});

// Mobile filter toggle
const filterBtn = document.getElementById('mobile-filter-btn');
const sidebar = document.getElementById('search-sidebar');

if (filterBtn && sidebar) {
    filterBtn.addEventListener('click', function () {
        this.classList.toggle('open');
        const isOpen = this.classList.contains('open');
        this.setAttribute('aria-expanded', isOpen);
        sidebar.classList.toggle('mobile-open');
    });
}