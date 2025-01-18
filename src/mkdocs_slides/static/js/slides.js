window.addEventListener('load', function() {
    document.querySelectorAll('.slides-deck').forEach(deck => {
        const slides = Array.from(deck.querySelectorAll('.slide'));
        const prevButton = deck.querySelector('.prev-slide');
        const nextButton = deck.querySelector('.next-slide');
        const progress = deck.querySelector('.slide-progress');
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

        // Button click handlers
        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            // Only handle keyboard if deck is visible in viewport
            const rect = deck.getBoundingClientRect();
            const isVisible = (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= window.innerHeight &&
                rect.right <= window.innerWidth
            );
            
            if (isVisible) {
                if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
                    prevSlide();
                    e.preventDefault();
                }
                if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === 'Space') {
                    nextSlide();
                    e.preventDefault();
                }
            }
        });

        // Initialize first slide
        showSlide(0);
    });
}); 