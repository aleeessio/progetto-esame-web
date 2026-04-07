const searchInput = document.getElementById('search-input');
const rows = document.querySelectorAll('tbody tr');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
});

function showTable(vehicleType) {
    document.querySelectorAll('.vehicle-table-container').forEach(function (el) {
        el.classList.remove('active');
    });

    const selectedTable = document.getElementById('table-' + vehicleType);
    if (selectedTable) {
        selectedTable.classList.add('active');
    }
}

//USO QUESTA FUNZIONE PER NON AVERE LA TRANSIZIONE "SPEZZATA" 
//QUABDO PASSO DALLA PAGINE LISTA_VEICOLI ALLA PAGINA DEL VEICOLO 
function goToVehicle(url) {
    const overlay = document.getElementById('page-overlay');

    overlay.classList.remove('is-revealed');
    overlay.classList.add('is-covering-prep');

    void overlay.offsetWidth;

    overlay.classList.remove('is-covering-prep');
    overlay.classList.add('is-covering-active');

    setTimeout(() => {
        window.location.href = url;
    }, 300);
}
