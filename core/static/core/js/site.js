const toTopButton = $("#toTopButton");
const sections = $('section'), nav = $('nav'), navHeight = nav.outerHeight();
const dropdown = $(".dropdown");
const newDescription = $('#id_new_description');
const description = $('#id_description');

// Temporary solution to file input field in user form - until django-bootstrap4 is fixed.
const file_input = $('#id_profile_photo');
const file_input_col = file_input.parent();
const file_error = file_input_col.parent().next();
file_error.appendTo(file_input_col);

dropdown.hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).fadeIn(500);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(500).fadeOut(500);
});

// // Add fade in for dropdown.
// dropdown.on('show.bs.dropdown', function() {
//     $(this).find('.dropdown-menu').first().stop(true, true).fadeIn(500);
// });
//
// // Add fade out for dropdown
// dropdown.on('hide.bs.dropdown', function() {
//     $(this).find('.dropdown-menu').first().stop(true, true).fadeOut(500);
// });


function setNewDescriptionVisibility() {
    /*
    Set enabled/disabled state of "new description" field in Smiley and Oopsy
    forms.
     */
    let optionSelected = description.find("option:selected").attr("value");
    if (optionSelected !== "Add new") {
        newDescription.prop('disabled', true);
        newDescription.prop('required', false);
    } else {
        newDescription.prop('disabled', false);
        newDescription.prop('required', true);
    }
}

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
        var top = $(this).offset().top - navHeight - 85,
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

// Activate on readiness of the document.
$(document).ready(function () {
    detectScroll();
    scrollToTop();
    autoActiveNavLinks();
    setNewDescriptionVisibility();
    description.on("change", setNewDescriptionVisibility);
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