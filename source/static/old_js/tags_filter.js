document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[name="tags"]');
    const resetButton = document.getElementById('reset-filters');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const selectedTags = Array.from(checkboxes)
                .filter(i => i.checked)
                .map(i => i.value);
            const params = new URLSearchParams();
            selectedTags.forEach(tag => params.append('tags', tag));

            const url = `${window.location.pathname}?${params.toString()}`;
            window.location.href = url;
        });
    });

    resetButton.addEventListener('click', () => {
        window.location.href = window.location.pathname;
    });
});