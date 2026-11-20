(() => {
    const showcase = document.getElementById("driverShowcase");
    const closeButton = document.getElementById("driverShowcaseClose");

    if (!showcase || !closeButton) return;

    const nameElement = document.getElementById("showcaseDriverName");
    const teamElement = document.getElementById("showcaseDriverTeam");
    const codeElement = document.getElementById("showcaseDriverCode");
    const numberElement = document.getElementById("showcaseDriverNumber");
    const nationalityElement = document.getElementById("showcaseDriverNationality");
    const imageElement = document.getElementById("showcaseDriverImage");
    const profileElement = document.getElementById("showcaseDriverProfile");

    const cards = document.querySelectorAll(".driver-card");

    let lastFocusedElement = null;

    // Open the driver showcase
    function openShowcase(card) {
        lastFocusedElement = card;

        const data = card.dataset;

        nameElement.textContent = data.driverName || "Driver";
        teamElement.textContent = data.driverTeam || "Formula One";
        codeElement.textContent = data.driverCode || "DRIVER PROFILE";
        numberElement.textContent = data.driverNumber || "—";
        nationalityElement.textContent = data.driverNationality || "NATIONALITY";

        imageElement.src = data.driverImage || "";
        imageElement.alt = data.driverName || "Driver portrait";

        // Display the official driver profile link if available
        if (data.driverUrl) {
            profileElement.href = data.driverUrl;
            profileElement.hidden = false;
        } else {
            profileElement.removeAttribute("href");
            profileElement.hidden = true;
        }

        // Match the showcase glow to the driver's team colour
        const accent = getComputedStyle(card)
            .getPropertyValue("--driver-accent")
            .trim();

        showcase.style.setProperty(
            "--showcase-accent",
            accent || "#e10600"
        );

        showcase.classList.add("is-open");
        showcase.setAttribute("aria-hidden", "false");

        document.body.classList.add("driver-showcase-open");

        closeButton.focus();
    }

    // Close the driver showcase
    function closeShowcase() {
        showcase.classList.remove("is-open");
        showcase.setAttribute("aria-hidden", "true");

        document.body.classList.remove("driver-showcase-open");

        // Return focus to the driver card that was clicked
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    }

    // Add click events to all driver cards
    cards.forEach((card) => {
        card.addEventListener("click", () => {
            openShowcase(card);
        });
    });

    // Close using the close button
    closeButton.addEventListener("click", closeShowcase);

    // Close when clicking the backdrop
    showcase.querySelectorAll("[data-showcase-close]").forEach((element) => {
        element.addEventListener("click", closeShowcase);
    });

    // Close when pressing Escape
    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape" &&
            showcase.classList.contains("is-open")
        ) {
            closeShowcase();
        }
    });
})();