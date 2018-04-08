var toTopButton = $("#toTopButton");

function detectScroll() {
    var offset = 800;
    var delay = 500;
    $(window).scroll(function () {
        if ($(window).scrollTop() >= offset) {
            console.log("showing button");
            // toTopButton.css({"display": "block"})
            toTopButton.fadeIn(delay);

        }
        else {
            console.log("hiding button");
            // toTopButton.css({"display": "none"})
            toTopButton.fadeOut(delay);
        }
    })
}

function scrollToTop() {
    toTopButton.click(function (event) {
        event.preventDefault();
        $("html, body").animate({scrollTop: 0}, 1000);
    })
}

$(document).ready(function () {
    detectScroll();
    scrollToTop();
});