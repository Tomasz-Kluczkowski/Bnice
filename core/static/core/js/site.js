var toTopButton = $("#toTopButton");
var sections = $('section'),
    nav = $('nav'),
    nav_height = nav.outerHeight();
var dropdown = $(".dropdown");


// Add fade in for dropdown.
dropdown.on('show.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).fadeIn(500);
});

// Add fade out for dropdown
dropdown.on('hide.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).fadeOut(500);
});

function detectScroll() {
    var offset = 800;
    var delay = 500;
    $(window).scroll(function () {
        if ($(window).scrollTop() >= offset) {
            toTopButton.fadeIn(delay);
        }
        else {
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

function setActiveClass() {
    sections.each(function () {
        var cur_pos = $(window).scrollTop();
        console.log("cur_pos:", cur_pos);
        var top = $(this).offset().top - nav_height - 85,
            bottom = top + $(this).outerHeight();

        if (cur_pos >= top && cur_pos <= bottom) {
            nav.find('a').removeClass('active');
            sections.removeClass('active');
            $(this).addClass('active');
            nav.find('a[href="#' + $(this).attr('id') + '"]').addClass('active');
        }
    });
}

// Automatic navigation links active state.
function autoActiveNavLinks() {
    $(window).on('scroll', setActiveClass)
}

$(document).ready(function () {
    detectScroll();
    scrollToTop();
    autoActiveNavLinks();
});


// Code for scrolling
$(document).ready(function() {

    // Select all links with hashes
    $('a[href*="#"]')
    // Remove links that don't actually link to anything
        .not('[href="#"]')
        .not('[href="#0"]')
        .click(function (event) {
            // On-page links
            if (
                location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
                &&
                location.hostname == this.hostname
            ) {
                // Figure out element to scroll to
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                // Does a scroll target exist?
                if (target.length) {
                    // Only prevent default if animation is actually gonna happen
                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 1000, function () {
                        // Callback after animation
                        // Must change focus!
                        var $target = $(target);
                        $target.focus();
                        if ($target.is(":focus")) { // Checking if the target was focused
                            return false;
                        } else {
                            $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                            $target.focus(); // Set focus again
                        }
                    });
                }
            }
        });
    });

// Check which nav item should be active on page reload.
setActiveClass();