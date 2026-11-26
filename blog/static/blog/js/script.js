document.addEventListener("DOMContentLoaded", function () {
    const navToggle = document.getElementById("navToggle");
    const mainNav = document.getElementById("mainNav");

    if (navToggle && mainNav) {
        navToggle.addEventListener("click", function () {
            mainNav.classList.toggle("open");
        });
    }

    const searchInput = document.getElementById("storySearch");
    const cards = document.querySelectorAll(".article-card");

    if (searchInput && cards.length) {
        searchInput.addEventListener("input", function () {
            const value = searchInput.value.toLowerCase().trim();

            cards.forEach(function (card) {
                const title = card.querySelector("h3");
                const text = title ? title.textContent.toLowerCase() : "";
                card.style.display = text.includes(value) ? "" : "none";
            });
        });
    }

    document.querySelectorAll("a[href*='/delete/']").forEach(function (link) {
        link.addEventListener("click", function (event) {
            if (!window.confirm("Delete this story permanently?")) {
                event.preventDefault();
            }
        });
    });
});
