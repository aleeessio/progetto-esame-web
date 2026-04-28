// Collapsible section for rental requests
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById('requests-toggle');
    const content = document.getElementById('requests-content');

    if (toggleBtn && content) {
        toggleBtn.addEventListener('click', function () {
            this.classList.toggle('active');

            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
});


// Heart button functionality for mini cards
document.querySelectorAll('.btn-favorite-mini').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        const vType = this.getAttribute('data-type');
        const vId = this.getAttribute('data-id');
        const card = this.closest('.mini-vehicle-card');

        fetch(`/toggle_favorite/${vType}/${vId}`, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.status === "removed") {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    setTimeout(() => card.remove(), 300);
                }
            });
    });
});