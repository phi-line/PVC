from fastapi import APIRouter, UploadFile

router = APIRouter()


@api.post("/upscale/{image_hash}")
async def upscale(image_hash: str, file: UploadFile):
    return {"filename": file.filename}
