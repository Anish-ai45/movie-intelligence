import httpx
from app.config import OMDB_API_KEY

BASE_URL = "https://www.omdbapi.com/"

async def search_movies(title: str):
    if not OMDB_API_KEY:
        return {"Response":"False","Error":"OMDB_API_KEY missing. Create .env with OMDB_API_KEY=..."}
    params = {"apikey": OMDB_API_KEY, "s": title}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        return r.json()

async def get_movie_details(imdb_id: str):
    if not OMDB_API_KEY:
        return {"Response":"False","Error":"OMDB_API_KEY missing. Create .env with OMDB_API_KEY=..."}
    params = {"apikey": OMDB_API_KEY, "i": imdb_id, "plot": "short"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        return r.json()
