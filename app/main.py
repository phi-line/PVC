from fastapi import Depends, FastAPI

from .routers import upscale

app = FastAPI()

app.include_router(upscale.router)

@app.get("/")
async def root():
    return {"msg": "hella world!"}