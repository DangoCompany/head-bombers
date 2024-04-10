from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from logics.timestamp import get_latest
from logics.image import post_image
from logics.artistry import get_artistry
from logics.yolo import calculate_explosiveness
from schemas import CalculateParameterReturnValue, GetLatestUpdateDateReturnValue

app = FastAPI()


@app.get("/get_image", response_class=FileResponse)
async def get_image(file_path: str):
    return file_path


@app.get("/get_latest_update_date", response_model=GetLatestUpdateDateReturnValue)
async def get_latest_update_date(user_name: str) -> GetLatestUpdateDateReturnValue:
    return get_latest(user_name)


@app.post("/post_image")
async def post_image(file: UploadFile) -> None:
    return post_image(file)


@app.post("/get_artistry", response_model=CalculateParameterReturnValue)
async def get_artistry(file_path: str) -> CalculateParameterReturnValue:
    return get_artistry(file_path)


@app.post("/get_explosiveness", response_model=CalculateParameterReturnValue)
async def get_explosiveness(file_path: str) -> CalculateParameterReturnValue:
    return await calculate_explosiveness(file_path)
