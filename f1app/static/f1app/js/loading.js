document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("site-loader");

    if (!loader) {
        return;
    }

    function hideLoader() {
        loader.classList.add("loader-hidden");
    }

    function showLoader() {
        loader.classList.remove("loader-hidden");
    }

    // Hide the loader when the browser finishes loading
    // the page and its dependent resources.
    if (document.readyState === "complete") {
        hideLoader();
    } else {
        window.addEventListener("load", hideLoader, {
            once: true
        });
    }

    // Show the loader when navigating to another page
    // on this website.
    document.addEventListener("click", function (event) {
        const link = event.target.closest("a");

        if (!link) {
            return;
        }

        if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.ctrlKey ||
            event.metaKey ||
            event.shiftKey ||
            event.altKey
        ) {
            return;
        }

        if (
            link.target === "_blank" ||
            link.hasAttribute("download") ||
            link.getAttribute("href")?.startsWith("#")
        ) {
            return;
        }

        const destination = new URL(link.href, window.location.href);

        if (destination.origin !== window.location.origin) {
            return;
        }

        if (
            destination.href === window.location.href ||
            destination.pathname === window.location.pathname &&
            destination.search === window.location.search &&
            destination.hash !== ""
        ) {
            return;
        }

        showLoader();
    });

    // Restore the page if the browser returns to it
    // using its back-forward cache.
    window.addEventListener("pageshow", function () {
        hideLoader();
    });
});