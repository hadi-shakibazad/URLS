from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from services.url_shrotener import find_url

router = APIRouter()

@router.get("/l/{code}")
async def home(code: str):
    if code is None and code == "":
        return {"msg": "no code given"}
    url, is_active = await find_url(code)
    if not is_active:
        return {"msg": "url is disabled"}
    return RedirectResponse(url)