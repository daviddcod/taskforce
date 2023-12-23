// Get the cookie consent banner and accept button
const consentBanner = document.getElementById('cookie-consent-banner');
const acceptButton = document.getElementById('accept-cookies-btn');

// Function to set a cookie to record user's consent
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Function to hide the banner and set the consent cookie when the user accepts
function acceptCookies() {
    setCookie('cookie_consent', 'accepted', 365); // Set a cookie named 'cookie_consent' with a one-year expiration
    consentBanner.style.display = 'none'; // Hide the banner
}

// Check if the user has already accepted cookies
if (document.cookie.indexOf('cookie_consent=accepted') === -1) {
    // Display the banner only if the user hasn't accepted cookies
    consentBanner.style.display = 'block';

    // Add click event listener to the accept button
    acceptButton.addEventListener('click', acceptCookies);
}
