export const API = import.meta.env.VITE_API_BASE_URL

export async function searhMovie(title) {
    const res = await fetch(`${API}/search?title=${encodeURIComponent(title)}`);
    if (!res.ok) throw new Error('Failed to fetch movie data');
    return res.json();
}

export async function getDetails(imdbId) {
    const res = await fetch(`${API}/details/${imdbId}`);
    if (!res.ok) throw new Error('Failed to fetch movie details');
    return res.json();
}

export async function getRecent(limit = 10) {
    const res = await fetch(`${API}/recent?limit=${limit}`);
    if (!res.ok) throw new Error('Failed to fetch recent movies');
    return res.json();
}