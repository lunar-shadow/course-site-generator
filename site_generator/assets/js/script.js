document.addEventListener('DOMContentLoaded', function() {
    // Sidebar functionality (only on course site)
    const sidebarToggle = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoTitle = document.getElementById('videoTitle');
    const videoItems = document.querySelectorAll('.video-item');

    if (sidebarToggle && sidebar && content && videoPlayer && videoTitle && videoItems) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            content.classList.toggle('full-width');
        });

        videoItems.forEach(item => {
            item.addEventListener('click', function() {
                const videoSrc = item.getAttribute('data-video-src');
                videoPlayer.src = videoSrc;

                const activeItem = document.querySelector('.video-item.active');
                if (activeItem) {
                    activeItem.classList.remove('active');
                }
                item.classList.add('active');

                videoTitle.textContent = item.textContent;
            });
        });
    }

    // Dark mode toggle functionality (common to both course site and homepage)
    const toggleDarkMode = document.getElementById('toggleDarkMode');
    if (toggleDarkMode) {
        toggleDarkMode.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode ? 'true' : 'false');
            toggleDarkMode.textContent = isDarkMode ? '☀️' : '🌙';
        });

        // Initialize dark mode state based on localStorage
        const storedDarkMode = localStorage.getItem('darkMode') === 'true';
        if (storedDarkMode) {
            document.body.classList.add('dark-mode');
            toggleDarkMode.textContent = '☀️';
        } else {
            document.body.classList.remove('dark-mode');
            toggleDarkMode.textContent = '🌙';
        }
    }
});
