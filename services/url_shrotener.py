import asyncio

import xxhash
from sqlalchemy import text, CursorResult

from db import get_session


def encode(txt: str) -> str:
    return xxhash.xxh32(txt).hexdigest()


async def add_url(url: str):
    code = encode(url)
    query = text(
        f"INSERT INTO urls (url, code) VALUES (:url, :code);"
    )
    async with get_session() as session:
        await session.execute(query, {"url": url, "code": code})
        await session.commit()

async def url_activation(url: str, activate: bool=True):
    query = text("UPDATE urls SET active = :activation WHERE url = :url;")
    async with get_session() as session:
        await session.execute(query, {"url": url, "activation": activate})
        await session.commit()

async def find_url(code: str):
    sql = text(f"SELECT url, code, active FROM urls WHERE code = :code")

    async with get_session() as session:
        data: CursorResult = await session.execute(sql, {"code": code})
    return data.fetchone()[0]
