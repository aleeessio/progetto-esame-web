// FIlTER SIDEBAR TOGGLE FOR MOBILE
document.addEventListener("DOMContentLoaded", function () {
    const filterBtn = document.getElementById("mobile-filter-btn");
    const sidebar = document.getElementById("search-sidebar");

    if (filterBtn && sidebar) {
        filterBtn.addEventListener("click", function () {
            const isExpanded = this.getAttribute("aria-expanded") === "true";
            this.setAttribute("aria-expanded", !isExpanded);
            sidebar.classList.toggle("active");
        });

        // Close sidebar when clicking outside
        document.addEventListener("click", function (e) {
            if (!sidebar.contains(e.target) && !filterBtn.contains(e.target)) {
                sidebar.classList.remove("active");
                filterBtn.setAttribute("aria-expanded", "false");
            }
        });
    }
});
