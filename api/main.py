from fastapi import Depends, FastAPI

from .routers import upscale

api = FastAPI()

api.include_router(upscale.router)

@api.get("/")
async def root():
    return {"msg": "hella world!"}