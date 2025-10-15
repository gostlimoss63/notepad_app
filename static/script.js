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
    const themeLink = document.getElementById("theme-link"); 
    const switchButton = document.getElementById("theme-switch");

    // Theme type definitions (desktop ↔ mobile pairs)
    const themes = {
        default: {
            desktop: "/static/style1.css",
            mobile: "/static/style1_mobile.css"
        },
        matrix: {
            desktop: "/static/style2.css",
            mobile: "/static/style2_mobile.css"
        },
        light: {
            desktop: "/static/style3.css",
            mobile: "/static/style3_mobile.css"
        }
    };

    const themeOrder = ["matrix", "light"];

    // Detect mobile device or narrow portrait ratio
    function isMobileDevice() {
        const ua = navigator.userAgent;
        const isTouch =
            /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua);
        const aspectRatio = window.innerWidth / window.innerHeight;
        const isPortraitPhone = aspectRatio < 0.7; // ~9:16 or narrower
        return isTouch || isPortraitPhone;
    }

    const isMobile = isMobileDevice();

    // Load saved theme (defaults to matrix)
    let currentTheme = localStorage.getItem("themeName") || "matrix";

    function applyTheme(name) {
        if (!themes[name]) name = "matrix";
        const selected = isMobile ? themes[name].mobile : themes[name].desktop;
        themeLink.href = selected;
        localStorage.setItem("themeName", name);
    }

    // Initial apply
    applyTheme(currentTheme);

    // Theme switch button
    switchButton.addEventListener("click", () => {
        const idx = themeOrder.indexOf(currentTheme);
        const next = (idx + 1) % themeOrder.length;
        currentTheme = themeOrder[next];
        applyTheme(currentTheme);
    });

    // Recheck if user rotates screen or resizes window
    window.addEventListener("resize", () => {
        const nowMobile = isMobileDevice();
        if (nowMobile !== isMobile) {
            applyTheme(currentTheme);
        }
    });
});

