// ========== utils.js ==========
// Common help functions between scripts.js and admin.js

// ===== Dynamically specify API link (supports localhost and GitHub Codespaces) =====
function getBaseUrl() {
    const { origin, hostname } = window.location;
    
    // Supports GitHub Codespaces
    if (origin.includes('github.dev') || origin.includes('app.github.dev')) {
        return origin.replace(/-(3000|5500|8080)\./, '-5000.');
    }
    
    if (hostname.match(/^\d+\.\d+\.\d+\.\d+$/)) {
        return `http://${hostname}:5000`;
    }
    
    return 'http://127.0.0.1:5000';
}

// ===== cookie function =====
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; path=/; expires=${expires.toUTCString()}; SameSite=Lax`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
}

function getToken() {
    return getCookie('token');
}

function isAuthenticated() {
    return !!getToken();
}

// ===== Security functions =====
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ===== Convert number to stars =====
function getStarRating(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

// ===== logout =====
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}
