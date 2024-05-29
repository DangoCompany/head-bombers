import re

from fastapi import UploadFile

from configs import IMAGES_DIR, TIMESTAMP_FILENAME
from hb_core.dtos.dto import PostImageReturnValue
from hb_core.error.error_code import ErrorCode
from hb_core.repositories.system import (
    exists_path,
    join_path,
    make_dir,
    read_json,
    write_binary,
    write_json,
)


def post_image(file: UploadFile) -> PostImageReturnValue:
    if not exists_path(IMAGES_DIR):
        make_dir(IMAGES_DIR)

    if file.content_type == "image/jpeg":
        # ファイル名が {UserName}_{YYYYMMDD}.jpg 形式かどうかを確認
        pattern = re.compile(r"(?P<username>[a-zA-Z0-9_]+)_(?P<date>\d{8})\.jpg")
        match = pattern.match(file.filename) if file.filename else None

        if match:
            user_name = match.group("username")
            date = match.group("date")

            if exists_path(TIMESTAMP_FILENAME):
                existing_data = read_json(TIMESTAMP_FILENAME)
            else:
                existing_data = {}
            existing_data[user_name] = date

            write_json(TIMESTAMP_FILENAME, existing_data)

            # ファイルの保存パスを生成
            save_path = join_path(IMAGES_DIR, file.filename)  # type: ignore

            # ファイルを保存
            write_binary(save_path, file.file.read())

            return PostImageReturnValue(error_codes=())

    # 正しい形式の画像ファイルがアップロードされていない場合のエラーメッセージ
    return PostImageReturnValue(error_codes=(ErrorCode.INVALID_IMAGE_FORMAT,))
