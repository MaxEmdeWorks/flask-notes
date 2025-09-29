$(document).ready(function() {
    var storageKey = 'flask-notes-dark-mode';
    var $html = $('html');
    var $icon = $('#darkModeIcon');

    // Get stored theme preference
    function getStoredTheme() {
        return localStorage && localStorage.getItem && localStorage.getItem(storageKey);
    }

    // Save theme preference
    function saveTheme(theme) {
        localStorage && localStorage.setItem && localStorage.setItem(storageKey, theme);
    }

    // Get system dark mode preference
    function getSystemPreference() {
        return matchMedia && matchMedia('(prefers-color-scheme: dark)').matches;
    }

    // Apply theme to the page
    function applyTheme(theme) {
        $html.attr('data-bs-theme', theme);

        // Update desktop icons
        $icon.removeClass('bi-moon bi-sun').addClass(theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon');

        // Update mobile icons and text
        var $mobileIcon = $('#darkModeIconMobile');
        var $mobileText = $('#darkModeTextMobile');
        if ($mobileIcon.length) {
            $mobileIcon.removeClass('bi-moon bi-sun').addClass(theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon');
            $mobileText.text(theme === 'dark' ? 'Light Mode' : 'Dark Mode');
        }

        saveTheme(theme);
    }

    // Toggle theme function
    function toggleTheme() {
        var currentTheme = $html.attr('data-bs-theme');
        var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }

    // Initialize theme on page load
    var initialTheme = getStoredTheme() || (getSystemPreference() ? 'dark' : 'light');
    applyTheme(initialTheme);

    // Handle dark mode toggle button clicks (desktop and mobile)
    $('#darkModeToggle, #darkModeToggleMobile').on('click', function(e) {
        e.preventDefault();
        toggleTheme();
    });

    // Listen for system theme changes
    if (matchMedia) {
        $(matchMedia('(prefers-color-scheme: dark)')).on('change', function() {
            if (!getStoredTheme()) {
                applyTheme(this.matches ? 'dark' : 'light');
            }
        });
    }
});
