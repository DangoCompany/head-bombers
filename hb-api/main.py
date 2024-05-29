from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from hb_core.logics.timestamp import get_latest as get_latest_logic
from hb_core.logics.image import post_image as post_image_logic
from hb_core.logics.artistry import get_artistry as get_artistry_logic
from hb_core.logics.yolo import calculate_explosiveness as calculate_explosiveness_logic
from hb_core.dtos.dto import CalculateParameterReturnValue, PostImageReturnValue, GetLatestUpdateDateReturnValue

app = FastAPI()


@app.get("/get_image", response_class=FileResponse)
async def get_image(file_path: str):
    return file_path


@app.get("/get_latest_update_date", response_model=GetLatestUpdateDateReturnValue)
async def get_latest_update_date(user_name: str) -> GetLatestUpdateDateReturnValue:
    return get_latest_logic(user_name)


@app.post("/post_image", response_model=PostImageReturnValue)
async def post_image(file: UploadFile) -> PostImageReturnValue:
    return post_image_logic(file)


@app.post("/get_artistry", response_model=CalculateParameterReturnValue)
async def get_artistry(file_path: str) -> CalculateParameterReturnValue:
    return get_artistry_logic(file_path)


@app.post("/get_explosiveness", response_model=CalculateParameterReturnValue)
async def get_explosiveness(file_path: str) -> CalculateParameterReturnValue:
    return calculate_explosiveness_logic(file_path)
