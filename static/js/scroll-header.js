document.addEventListener('DOMContentLoaded', function() {
    let lastScrollTop = 0;
    const header = document.querySelector('.room__top');
    const scrollThreshold = 60; // Minimum scroll amount before hiding/showing
    let isScrolling;

    // Check if header exists
    if (!header) {
        console.log('Header element not found');
        return;
    }

    // Add initial visible class
    header.classList.add('room__top--visible');

    window.addEventListener('scroll', () => {
        clearTimeout(isScrolling);
        
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        
        try {
            // Show header immediately when scrolling up
            if (currentScroll < lastScrollTop) {
                header.classList.remove('room__top--hidden');
                header.classList.add('room__top--visible');
            } 
            // Hide header when scrolling down past threshold
            else if (currentScroll > lastScrollTop && currentScroll > scrollThreshold) {
                header.classList.add('room__top--hidden');
                header.classList.remove('room__top--visible');
            }
            
            lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // For Mobile or negative scrolling
            
            // Set a timeout to show header after scrolling stops
            isScrolling = setTimeout(() => {
                header.classList.remove('room__top--hidden');
                header.classList.add('room__top--visible');
            }, 1500);
        } catch (error) {
            console.error('Error handling scroll:', error);
        }
    }, { passive: true });
}); 