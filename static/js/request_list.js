// VIEW REQUESTS MESSAGES 
function toggleMessage(rowId, btnElement) {
    const messageRow = document.getElementById(rowId);

    if (messageRow.classList.contains('show')) {
        messageRow.classList.remove('show');
        btnElement.textContent = 'View';
        btnElement.classList.remove('active');
    } else {
        messageRow.classList.add('show');
        btnElement.textContent = 'Hide';
        btnElement.classList.add('active');
    }
}

// REQUEST SEARCH 
const searchInput = document.getElementById('search-input');
const rows = document.querySelectorAll('tbody tr');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    rows.forEach(row => {
        let text = '';
        for (let i = 0; i < 6; i++) {
            if (row.cells[i]) {
                text += row.cells[i].innerText.toLowerCase() + ' ';
            }
        }
        row.style.display = text.includes(query) ? '' : 'none';
    });
});
