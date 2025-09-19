document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const notesContainer = document.getElementById("notes-container");

    searchInput.addEventListener("input", () => {
        const query = searchInput.value;
        fetch(`/search_notes?q=${encodeURIComponent(query)}`)
            .then(response => response.text())
            .then(html => {
                notesContainer.innerHTML = html;
            });
    });
});
