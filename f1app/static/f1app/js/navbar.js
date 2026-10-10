document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".header");

    if (!header) return;

    let lastScrollY = window.scrollY;
    const scrollThreshold = 10;

    window.addEventListener("scroll", function () {
        const currentScrollY = window.scrollY;
        const difference = currentScrollY - lastScrollY;

        // Always show the navbar at the top of the page
        if (currentScrollY <= 50) {
            header.classList.remove("nav-hidden");
            header.classList.add("nav-visible");
        } else if (difference > scrollThreshold) {
            // Scrolling down: hide navbar
            header.classList.add("nav-hidden");
            header.classList.remove("nav-visible");
        } else if (difference < -scrollThreshold) {
            // Scrolling up: show navbar
            header.classList.remove("nav-hidden");
            header.classList.add("nav-visible");
        }

        lastScrollY = currentScrollY;
    }, { passive: true });
});