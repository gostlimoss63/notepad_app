document.addEventListener("DOMContentLoaded", () => {
    const notesContainer = document.getElementById("notes-container");

    // Handle active notes search
    const activeSearch = document.getElementById("search");
    if (activeSearch) {
        activeSearch.addEventListener("input", () => {
            const query = activeSearch.value;
            fetch(`/search_notes?q=${encodeURIComponent(query)}&completed=false`)
                .then(response => response.text())
                .then(html => {
                    notesContainer.innerHTML = html;
                });
        });
    }

    // Handle completed notes search
    const completedSearch = document.getElementById("completed_search");
    if (completedSearch) {
        completedSearch.addEventListener("input", () => {
            const query = completedSearch.value;
            fetch(`/search_notes?q=${encodeURIComponent(query)}&completed=true`)
                .then(response => response.text())
                .then(html => {
                    notesContainer.innerHTML = html;
                });
        });
    }
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
