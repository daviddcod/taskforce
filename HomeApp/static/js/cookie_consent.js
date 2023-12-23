document.addEventListener('DOMContentLoaded', function() {
    const consentBanner = document.getElementById('cookie-consent-banner');
    const acceptButton = document.getElementById('accept-cookies-btn');

    function acceptCookies() {
        fetch('/set_cookie', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    consentBanner.style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
    }

    if (acceptButton) {
        acceptButton.addEventListener('click', acceptCookies);
    }
});
