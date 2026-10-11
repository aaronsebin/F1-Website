
document.addEventListener("DOMContentLoaded", () => {
    const showcase = document.getElementById("teamShowcase");
    const closeButton = document.getElementById("showcaseClose");
    const carImage = document.getElementById("showcaseCar");
    const teamName = document.getElementById("showcaseTeamName");
    const teamCode = document.getElementById("showcaseTeamCode");
    const caption = document.getElementById("showcaseCaption");
    const teamIndex = document.getElementById("showcaseIndex");

    if (
        !showcase ||
        !closeButton ||
        !carImage ||
        !teamName ||
        !teamCode ||
        !caption ||
        !teamIndex
    ) {
        return;
    }

    const teamColors = {
        "mclaren": "#ff8000",
        "mercedes": "#00d2be",
        "red-bull-racing": "#4263ff",
        "ferrari": "#e10600",
        "williams": "#008cff",
        "racing-bulls": "#648cff",
        "aston-martin": "#006f62",
        "haas": "#d2d2d7",
        "audi": "#c0c0c8",
        "alpine": "#e005a6",
        "cadillac": "#bcbcc3"
    };

    let previouslyFocusedCard = null;

    function openShowcase(card) {
        previouslyFocusedCard = card;

        const name = card.dataset.teamName || "Formula One Team";
        const code = card.dataset.teamCode || "TEAM";
        const image = card.dataset.teamImage;
        const slug = card.dataset.teamSlug || "";

        teamName.textContent = name;
        teamCode.textContent = code;
        caption.textContent = `${code} / CONSTRUCTOR`;

        carImage.src = image || "";
        carImage.alt = `${name} Formula One car`;

        const cards = [...document.querySelectorAll(".team-card")];
        const position = cards.indexOf(card) + 1;

        teamIndex.textContent =
            `${String(position).padStart(2, "0")} / ` +
            `${String(cards.length).padStart(2, "0")}`;

        showcase.style.setProperty(
            "--showcase-accent",
            teamColors[slug] || "#e10600"
        );

        showcase.classList.add("is-open");
        showcase.setAttribute("aria-hidden", "false");
        document.body.classList.add("team-showcase-open");

        closeButton.focus();
    }

    function closeShowcase() {
        showcase.classList.remove("is-open");
        showcase.setAttribute("aria-hidden", "true");
        document.body.classList.remove("team-showcase-open");

        if (previouslyFocusedCard) {
            previouslyFocusedCard.focus();
        }
    }

    document.querySelectorAll(".team-card").forEach((card) => {
        card.addEventListener("click", (event) => {
            event.preventDefault();
            openShowcase(card);
        });
    });

    closeButton.addEventListener("click", closeShowcase);

    // Clicking the dark background closes the showcase.
    showcase.querySelector(".showcase-backdrop")
        ?.addEventListener("click", closeShowcase);

    // Escape key also closes the showcase.
    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape" &&
            showcase.classList.contains("is-open")
        ) {
            closeShowcase();
        }
    });
});
