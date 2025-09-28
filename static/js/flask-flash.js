$(document).ready(function() {
    // Auto-hide flash messages after 5 seconds
    $('.flash-popup').each(function() {
        var $message = $(this);
        setTimeout(function() {
            // Add fade out animation
            $message.css('animation', 'fadeOutToRight 0.5s ease-in forwards');
            // Remove element after animation
            setTimeout(function() {
                $message.remove();
            }, 500);
        }, 5000); // 5 seconds delay
    });

    // Handle manual close button clicks
    $('.flash-popup .btn-close').on('click', function() {
        var $message = $(this).closest('.flash-popup');
        $message.css('animation', 'fadeOutToRight 0.3s ease-in forwards');
        setTimeout(function() {
            $message.remove();
        }, 300);
    });
});
