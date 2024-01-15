import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import router as auth_router
from src.users import router as user_router
from src.social import router as social_router

app = FastAPI()
app.mount("/media", StaticFiles(directory="../media",), name="media")

app.include_router(user_router.router, tags=['user'], prefix='/user')
app.include_router(auth_router.router, tags=['auth'], prefix='/auth')
app.include_router(social_router.router, tags=['social'], prefix='/social')


@app.on_event("startup")
async def startup():
    from config import settings
    import os
    media_dir = settings.MEDIA.MEDIA_DIR
    if not os.path.exists(media_dir):
        os.mkdir(media_dir)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
