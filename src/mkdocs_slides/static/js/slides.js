document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.slides-container').forEach(container => {
        const slides = container.querySelectorAll('.slide');
        const prevButton = container.querySelector('.prev-slide');
        const nextButton = container.querySelector('.next-slide');
        const fullscreenButton = container.querySelector('.fullscreen');
        const progress = container.querySelector('.slide-progress');
        let currentSlide = 0;

        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
            progress.textContent = `${index + 1} / ${slides.length}`;
            prevButton.disabled = index === 0;
            nextButton.disabled = index === slides.length - 1;
        }

        showSlide(0);

        prevButton?.addEventListener('click', () => {
            if (currentSlide > 0) {
                currentSlide--;
                showSlide(currentSlide);
            }
        });

        nextButton?.addEventListener('click', () => {
            if (currentSlide < slides.length - 1) {
                currentSlide++;
                showSlide(currentSlide);
            }
        });

        container.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') prevButton.click();
            if (e.key === 'ArrowRight') nextButton.click();
        });

        fullscreenButton?.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                container.requestFullscreen();
                container.classList.add('fullscreen');
            } else {
                document.exitFullscreen();
                container.classList.remove('fullscreen');
            }
        });

        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement) {
                container.classList.remove('fullscreen');
            }
        });
    });
}); 