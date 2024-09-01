document.addEventListener('DOMContentLoaded', () => {
    function updateCountdown() {
        document.querySelectorAll('[id^=countdown-]').forEach((element) => {
            const duration = parseInt(element.textContent, 10);
            const interval = setInterval(() => {
                if (duration <= 0) {
                    clearInterval(interval);
                    element.textContent = 'Reservation Expired';
                } else {
                    duration--;
                    element.textContent = duration + ' minutes left';
                }
            }, 60000); // Update every minute
        });
    }
    updateCountdown();
});
