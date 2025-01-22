window.addEventListener('load', function() {
    // Track the active deck globally
    let activeDeck = null;

    // Handle orientation changes
    function handleOrientation() {
        const isPortrait = window.matchMedia("(orientation: portrait)").matches;
        document.querySelectorAll('.slides-deck').forEach(deck => {
            if (isPortrait) {
                deck.classList.add('portrait');
                // Exit fullscreen if active
                if (deck.classList.contains('fullscreen')) {
                    deck.querySelector('.fullscreen-toggle').click();
                }
            } else {
                deck.classList.remove('portrait');
            }
        });
    }

    // Listen for orientation changes
    window.addEventListener('orientationchange', handleOrientation);
    window.addEventListener('resize', handleOrientation);
    handleOrientation(); // Initial check

    document.querySelectorAll('.slides-deck').forEach(deck => {
        const slides = Array.from(deck.querySelectorAll('.slide'));
        const prevButton = deck.querySelector('.prev-slide');
        const nextButton = deck.querySelector('.next-slide');
        const progress = deck.querySelector('.slide-progress');
        const fullscreenBtn = deck.querySelector('.fullscreen-toggle');
        const overviewBtn = deck.querySelector('.overview-toggle');
        const overviewCloseBtn = deck.querySelector('.overview-close');
        let currentIndex = 0;

        function showSlide(index) {
            slides.forEach(slide => slide.style.display = 'none');
            slides[index].style.display = 'block';
            progress.textContent = `${index + 1} / ${slides.length}`;
            prevButton.disabled = index === 0;
            nextButton.disabled = index === slides.length - 1;
        }

        function prevSlide() {
            if (currentIndex > 0) {
                currentIndex--;
                showSlide(currentIndex);
            }
        }

        function nextSlide() {
            if (currentIndex < slides.length - 1) {
                currentIndex++;
                showSlide(currentIndex);
            }
        }

        function toggleFullscreen() {
            deck.classList.toggle('fullscreen');
            if (deck.classList.contains('fullscreen')) {
                fullscreenBtn.textContent = '⛶';
                fullscreenBtn.title = 'Exit fullscreen';
            } else {
                fullscreenBtn.textContent = '⛶';
                fullscreenBtn.title = 'Enter fullscreen';
            }
            window.dispatchEvent(new Event('resize'));
        }

        function toggleOverview() {
            deck.classList.toggle('overview-active');
            if (deck.classList.contains('overview-active')) {
                overviewBtn.textContent = '×';
                overviewBtn.title = 'Close overview (O)';
            } else {
                overviewBtn.textContent = '⊞';
                overviewBtn.title = 'Show overview (O)';
            }
        }

        // Set active deck on any interaction
        deck.addEventListener('mouseenter', () => {
            activeDeck = deck;
        });

        deck.addEventListener('click', () => {
            activeDeck = deck;
        });

        // Button click handlers
        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);
        fullscreenBtn.addEventListener('click', toggleFullscreen);
        overviewBtn.addEventListener('click', toggleOverview);

        // Add click handlers for overview slides
        deck.querySelectorAll('.overview-slide').forEach(slide => {
            slide.addEventListener('click', () => {
                const index = parseInt(slide.dataset.index);
                showSlide(index);
                toggleOverview();
            });
        });

        // Add click handler for overview close button
        overviewCloseBtn.addEventListener('click', toggleOverview);

        // Keyboard navigation - moved to global handler
        showSlide(0);
    });

    // Global keyboard handler
    document.addEventListener('keydown', function(e) {
        if (!activeDeck) return;

        // Only handle keyboard if active deck is visible or in fullscreen
        const rect = activeDeck.getBoundingClientRect();
        const isVisible = (
            activeDeck.classList.contains('fullscreen') || 
            (rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= window.innerHeight &&
            rect.right <= window.innerWidth)
        );
        
        if (!isVisible) return;

        const controls = {
            prevSlide: activeDeck.querySelector('.prev-slide'),
            nextSlide: activeDeck.querySelector('.next-slide')
        };

        switch (e.key) {
            case 'ArrowLeft':
            case 'PageUp':
                if (!controls.prevSlide.disabled) {
                    controls.prevSlide.click();
                    e.preventDefault();
                }
                break;
            case 'ArrowRight':
            case 'PageDown':
            case ' ': // Space
                if (!controls.nextSlide.disabled) {
                    controls.nextSlide.click();
                    e.preventDefault();
                }
                break;
            case 'Escape':
                if (activeDeck.classList.contains('overview-active')) {
                    activeDeck.querySelector('.overview-toggle').click();
                    e.preventDefault();
                } else if (activeDeck.classList.contains('fullscreen')) {
                    activeDeck.querySelector('.fullscreen-toggle').click();
                    e.preventDefault();
                }
                break;
            case 'o':
            case 'O':
                toggleOverview();
                e.preventDefault();
                break;
        }
    });
}); 