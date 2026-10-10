document.querySelectorAll(".inline-form").forEach(form => {
    form.addEventListener("submit", (event) => {
        if (event.target.dataset.irreversible === "true") {
            const conf = confirm("This operation is irreversible.")
            if (conf === false) {
                event.preventDefault();
            }
        }
    });
});