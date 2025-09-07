from fastapi import FastAPI
from app.services.omdb import search_movies, get_movie_details
from app.models import Movie, SearchResults, SearchHistory
from fastapi import HTTPException
from app.db import init_db, get_session
from sqlmodel import Session, select
from fastapi import Depends,Query
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Any cleanup code can go here

app = FastAPI(title="Movie Intelligence API", 
              description="API for searching movies and getting movie details", 
              version="1.0.0",
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/search", response_model=SearchResults)
async def search(title: str, session : Session = Depends(get_session)):
    data = await search_movies(title)
    if data.get("Response") != "True":
        raise HTTPException(status_code=404, detail="Movies not found")
    results = [
        Movie(
            title=item["Title"],
            year=item["Year"],
            imdb_id=item["imdbID"],
            poster=item["Poster"]
        )
            for item in data["Search"]
    ]
    # Log the search
    if results:
        row = SearchHistory(title=title)
        session.add(row)
        session.commit()
    return SearchResults(results= results)

@app.get("/details/{imdb_id}", response_model=Movie)
async def get_details(imdb_id: str):
    data = await get_movie_details(imdb_id)
    if data.get("Response") != "True":
        raise HTTPException(status_code=404, detail="Movie not found")
    return Movie(
        title=data["Title"],
        year= data["Year"],
        imdb_id=data["imdbID"],
        poster=data["Poster"],
        plot=data["Plot"],
        genre=data["Genre"],
        director=data["Director"],
        actors=data["Actors"],
        imdb_rating=data["imdbRating"] 
    )

@app.get("/recent", response_model=list[str])
def recent(session : Session = Depends(get_session), limit: int = Query(10,ge=1,le=50)):
    stmt = select(SearchHistory).order_by(SearchHistory.timestamp.desc()).limit(limit)
    rows = list(session.exec(stmt))
    return [r.title for r in rows]