from typing import List
from sqlmodel import select, Session
from app.db import get_session
from app.models import SearchHistory


def log_search(session : Session, title : str) -> SearchHistory:
    search_entry = SearchHistory(title=title)
    session.add(search_entry)
    session.commit()
    session.refresh(search_entry)
    return search_entry

def get_recent(session : Session, limit : int = 10) -> List[SearchHistory]:
    stmt = select(SearchHistory).order_by(SearchHistory.created_at.desc()).limit(limit)
    return list(session.exec(stmt))