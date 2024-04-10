import re
from fastapi import UploadFile

from repositories.system import exists_path, join_path, make_dir, read_json, write_json, write_binary
from configs import IMAGES_DIR, TIMESTAMP_FILENAME


def post_image(file: UploadFile):
    if not exists_path(IMAGES_DIR):
        make_dir(IMAGES_DIR)

    if file.content_type == "image/jpeg":
        # ファイル名が {UserName}_{YYYYMMDD}.jpg 形式かどうかを確認
        pattern = re.compile(r'(?P<username>[a-zA-Z0-9_]+)_(?P<date>\d{8})\.jpg')
        match = pattern.match(file.filename)

        if match:
            user_name = match.group('username')
            date = match.group('date')

            if exists_path(TIMESTAMP_FILENAME):
                existing_data = read_json(TIMESTAMP_FILENAME)
            else:
                existing_data = {}
            existing_data[user_name] = date

            write_json(TIMESTAMP_FILENAME, existing_data)

            # ファイルの保存パスを生成
            save_path = join_path(IMAGES_DIR, file.filename)

            # ファイルを保存
            write_binary(save_path, file.file.read())

            return {"message": f"File '{file.filename}' saved as JPEG in './images' directory."}

    # JPEG 形式のファイルがアップロードされていない場合のエラーメッセージ
    return {"message": "No JPEG file uploaded."}
