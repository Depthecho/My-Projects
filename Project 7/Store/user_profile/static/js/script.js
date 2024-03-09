<script>
    function toggleTheme() {
        const body = document.body;
        const themeIndicator = document.querySelector('.theme-indicator');
        const isDarkMode = body.classList.contains('dark-mode');

        if (isDarkMode) {
            themeIndicator.classList.remove('fa-sun');
            themeIndicator.classList.add('fa-moon');
        } else {
            themeIndicator.classList.remove('fa-moon');
            themeIndicator.classList.add('fa-sun');
        }

        body.classList.toggle('dark-mode');
        const newMode = isDarkMode ? 'light' : 'dark';
        localStorage.setItem('theme', newMode);
    }

    document.querySelector('.swap-theme').addEventListener('click', toggleTheme);

    function applySavedTheme() {
        const body = document.body;
        const themeIndicator = document.querySelector('.theme-indicator');
        const savedTheme = localStorage.getItem('theme');

        if (savedTheme === 'dark') {
            body.classList.add('dark-mode');
            themeIndicator.classList.add('fa-sun');
        } else {
            body.classList.remove('dark-mode');
            themeIndicator.classList.add('fa-moon');
        }
    }

    document.addEventListener('DOMContentLoaded', applySavedTheme);
</script>