document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    // Sidebar functionality (only on course site)
    const sidebarToggle = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoTitle = document.getElementById('videoTitle');
    const videoItems = document.querySelectorAll('.video-item');

    if (sidebarToggle && sidebar && content && videoPlayer && videoTitle && videoItems) {
        console.log('Sidebar elements found');

        sidebarToggle.addEventListener('click', function() {
            console.log('Sidebar toggle clicked');
            sidebar.classList.toggle('collapsed');
            content.classList.toggle('full-width');
        });

        videoItems.forEach(item => {
            item.addEventListener('click', function() {
                const videoSrc = item.getAttribute('data-video-src');
                console.log('Video item clicked:', videoSrc);
                videoPlayer.src = videoSrc;

                const activeItem = document.querySelector('.video-item.active');
                if (activeItem) {
                    activeItem.classList.remove('active');
                }
                item.classList.add('active');

                videoTitle.textContent = item.textContent;
            });
        });
    } else {
        console.log('Sidebar elements not found');
    }

    // Dark mode toggle functionality (common to both course site and homepage)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        console.log('Dark mode toggle found');
        darkModeToggle.addEventListener('change', function() {
            console.log('Dark mode toggle changed');
            const isDarkMode = darkModeToggle.checked;
            document.body.classList.toggle('dark-mode', isDarkMode);
            localStorage.setItem('darkMode', isDarkMode ? 'true' : 'false');
        });

        // Initialize dark mode state based on localStorage
        const storedDarkMode = localStorage.getItem('darkMode') === 'true';
        document.body.classList.toggle('dark-mode', storedDarkMode);
        darkModeToggle.checked = storedDarkMode;
        console.log('Dark mode initialized to', storedDarkMode);
    } else {
        console.log('Dark mode toggle not found');
    }
});
