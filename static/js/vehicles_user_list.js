const searchInput = document.getElementById('search-input');
const rows = document.querySelectorAll('tbody tr');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
});