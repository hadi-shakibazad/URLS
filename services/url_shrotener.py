import xxhash
from sqlalchemy import text, CursorResult
import re

from db import get_session


def is_valid_url(url: str) -> bool:
    patten = r"https?:\/\/[\w\-]+(\.[\w\-]+)+(:\d+)?(\/[^\s]*)?"
    return bool(re.match(patten, url))

def encode(txt: str) -> str:
    return xxhash.xxh32(txt).hexdigest()


async def add_url(url: str, user_id: int):
    if not is_valid_url(url):
        return
    code = encode(url)
    query = text(
        "INSERT INTO urls (url, code, user_id) VALUES (:url, :code, :user_id);"
    )
    async with get_session() as session:
        await session.execute(query, {"url": url, "code": code, "user_id": user_id})
        await session.commit()
    return code

async def url_activation(code: str, activate: bool=True):
    query = text("UPDATE urls SET active = :activation WHERE code = :code;")
    async with get_session() as session:
        await session.execute(query, {"code": code, "activation": activate})
        await session.commit()
    return activate

async def find_url(code: str) -> tuple[str, bool]:
    sql = text("SELECT url, code, active FROM urls WHERE code = :code")

    async with get_session() as session:
        data: CursorResult = await session.execute(sql, {"code": code})
    record = data.fetchone()
    return (
        record[0],
        bool(record[-1])
    )

async def owned_urls(user_id: int):
    sql = text("SELECT url, code, active FROM urls WHERE user_id = :user_id")

    async with get_session() as session:
        data: CursorResult = await session.execute(sql, {"user_id": user_id})
    return data.fetchall()

async def is_owned(url: str, user_id: int):

    sql = text("SELECT url, code, active FROM urls WHERE user_id=:user_id AND url=:url")

    async with get_session() as session:
        data: CursorResult = await session.execute(sql, {"user_id": user_id, "url": url})
    if len(data.fetchall()) > 0:
        return True
    return False