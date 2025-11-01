// Custom JavaScript for AI Tracks

$(document).ready(function() {
    // Back to Top Button
    const backToTopButton = $('<button>')
        .addClass('btn btn-primary back-to-top')
        .html('<i class="fas fa-arrow-up"></i>')
        .attr('title', 'Back to Top')
        .appendTo('body');

    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            backToTopButton.addClass('show');
        } else {
            backToTopButton.removeClass('show');
        }
    });

    backToTopButton.click(function() {
        $('html, body').animate({ scrollTop: 0 }, 600);
        return false;
    });

    // Smooth Scrolling for Anchor Links
    $('a[href^="#"]').on('click', function(e) {
        const target = $(this.hash);
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 600);
        }
    });

    // Initialize Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Loading Spinner for Forms
    $('form').on('submit', function() {
        const submitButton = $(this).find('button[type="submit"]');
        submitButton.prop('disabled', true);
        submitButton.html('<span class="spinner-border spinner-border-sm me-2"></span>Sending...');
    });

    // Auto-hide Alerts
    $('.alert').each(function() {
        const alert = $(this);
        setTimeout(function() {
            alert.fadeOut('slow');
        }, 5000);
    });
});
