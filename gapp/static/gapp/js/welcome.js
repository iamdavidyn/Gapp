// Simple interactions and animations for the welcome page
document.addEventListener('DOMContentLoaded', function () {
    // float the logo
    const logo = document.getElementById('gcash-logo');
    if (logo) logo.classList.add('logo-float', 'logo-glow');

    // Intersection reveal for the card
    const card = document.querySelector('.welcome-card');
    if (card) {
        card.style.opacity = 0;
        requestAnimationFrame(() => {
            card.style.transition = 'opacity .7s ease, transform .7s ease';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        });
    }

    // Button ripple effect
    const buttons = document.querySelectorAll('.welcome-link, .welcome-secondary');
    buttons.forEach(btn => {
        btn.classList.add('btn-ripple');
        btn.addEventListener('click', function (e) {
            const rect = btn.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            btn.appendChild(ripple);
            setTimeout(() => ripple.remove(), 650);
        });
    });
});
