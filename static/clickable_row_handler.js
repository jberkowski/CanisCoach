document.querySelectorAll(".clickable-row").forEach(row => {
    row.addEventListener("click", (event) => {
        if (event.target.closest("a, form") === null) {
            window.location.href = row.dataset.href;
        }
    });
});