import uvicorn
from fastapi import FastAPI

from routes.home import router as home_router
from routes.telegram import router as telegram_router


app = FastAPI()
app.include_router(home_router)
app.include_router(telegram_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)