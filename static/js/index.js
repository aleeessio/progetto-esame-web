// Gestione selezione veicolo nella homepage

const cards    = document.querySelectorAll('.selector-card');
const cta      = document.getElementById('selector-cta');
const searchBtn = document.getElementById('search-btn');

let selected = null;

cards.forEach(card => {
    card.addEventListener('click', () => {
        // Deseleziona tutti
        cards.forEach(c => c.classList.remove('selected'));

        // Seleziona quello cliccato
        card.classList.add('selected');
        selected = card.dataset.type;

        // Aggiorna href del bottone
        searchBtn.href = `/search?type=${selected}`;

        // Mostra il bottone con animazione
        cta.classList.add('visible');
    });
});
