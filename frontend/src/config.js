// frontend/src/config.js
// This file handles API URLs for both development and production

const getApiUrl = () => {
    // For production (Vercel) - use your Render URL
    if (process.env.NODE_ENV === 'production') {
        return 'https://brent-oil-api.onrender.com';
    }

    // For local development
    return 'http://localhost:5000';
};

export const API_BASE_URL = getApiUrl();

// Specific endpoint URLs
export const API_ENDPOINTS = {
    prices: `${API_BASE_URL}/api/prices`,
    events: `${API_BASE_URL}/api/events`,
    changePoint: `${API_BASE_URL}/api/change-point`,
    summary: `${API_BASE_URL}/api/summary`,
    volatility: `${API_BASE_URL}/api/volatility`,
    eventImpact: (id) => `${API_BASE_URL}/api/event-impact/${id}`,
    predictions: `${API_BASE_URL}/api/price-predictions`,
};