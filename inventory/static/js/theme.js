document.addEventListener('DOMContentLoaded', function () {
    const root = document.documentElement;
    const toggleButton = document.getElementById('theme-toggle');

    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        root.setAttribute('data-theme', 'dark');
    } else {
        root.setAttribute('data-theme', 'light');
    }

    updateThemeButtonText();

    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            const currentTheme = root.getAttribute('data-theme');

            if (currentTheme === 'dark') {
                root.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            } else {
                root.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }

            updateThemeButtonText();
        });
    }

    function updateThemeButtonText() {
        if (!toggleButton) return;

        const currentTheme = root.getAttribute('data-theme');

        if (currentTheme === 'dark') {
            toggleButton.textContent = 'Светлая тема';
        } else {
            toggleButton.textContent = 'Тёмная тема';
        }
    }
});
