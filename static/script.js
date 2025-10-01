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

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("completed_search");
    const notesContainer = document.getElementById("notes-container");

    searchInput.addEventListener("input", () => {
        const query = searchInput.value;
        fetch(`/search_completed_notes?q=${encodeURIComponent(query)}`)
            .then(response => response.text())
            .then(html => {
                notesContainer.innerHTML = html;
            });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggle-theme");
    const themeLink = document.getElementById("theme-style");

    // List of available themes
    const themes = [
        "/static/style1.css",
        "/static/style2.css",
        "/static/style3.css"
    ];

    // Load saved theme or fallback to first
    let currentTheme = localStorage.getItem("theme") || themes[0];
    themeLink.href = currentTheme;

    toggleBtn.addEventListener("click", () => {
        let idx = themes.indexOf(themeLink.getAttribute("href"));
        idx = (idx + 1) % themes.length;  // cycle through themes
        themeLink.href = themes[idx];
        localStorage.setItem("theme", themes[idx]);
    });
});
