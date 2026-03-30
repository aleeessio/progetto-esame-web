function showForm(type) {

    const imageSection = document.getElementById('image-upload-section');
    imageSection.style.display = type ? 'block' : 'none';

    document.querySelectorAll('.vehicle-form').forEach(f => {
        f.classList.remove('active');
        f.querySelectorAll('input, select').forEach(field => { field.disabled = true; });
    });

    document.getElementById('btn-submit').classList.remove('active');

    if (type) {
        const form = document.getElementById('form-' + type);
        if (form) {
            form.classList.add('active');
            document.getElementById('btn-submit').classList.add('active');
            form.querySelectorAll('input, select').forEach(field => { field.disabled = false; });
        }
    }

}