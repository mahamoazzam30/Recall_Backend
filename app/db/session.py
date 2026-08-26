import socket
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

settings = get_settings()

_url = make_url(settings.database_url)


def _resolve_ipv4(host: str) -> str | None:
    """Some networks route this host's IPv6 addresses to a dead end that
    times out silently instead of failing fast, adding tens of seconds
    (sometimes minutes) before libpq would otherwise fall back to a working
    IPv4 address. Resolving to IPv4 up front and connecting directly to it
    (via libpq's `hostaddr`, with `host` kept for TLS verification) skips
    those dead IPv6 attempts entirely.
    """
    try:
        return socket.getaddrinfo(host, _url.port or 5432, socket.AF_INET)[0][4][0]
    except OSError:
        return None


_connect_args: dict[str, str] = {}
if _url.host:
    ipv4 = _resolve_ipv4(_url.host)
    if ipv4:
        _connect_args["hostaddr"] = ipv4

engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
