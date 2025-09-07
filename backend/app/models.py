from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Movie(BaseModel):
    title : str
    year : Optional[str] = None
    imdb_id : Optional[str] = None
    poster : Optional[str] = None
    plot : Optional[str] = None
    genre : Optional[str] = None
    director : Optional[str] = None
    actors : Optional[str] = None
    imdb_rating : Optional[str] = None

class SearchResults(BaseModel):
    results: List[Movie]


# SearchHistory model for database
class SearchHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)