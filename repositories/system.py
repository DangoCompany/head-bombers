import os
import json


def exists_path(filename: str) -> bool:
    return os.path.exists(filename)


def join_path(dirname: str, filename: str) -> str:
    return os.path.join(dirname, filename)


def make_dir(dirname: str) -> None:
    os.makedirs(dirname)


def read_json(filename: str) -> dict:
    with open(filename, 'r') as json_file:
        return json.load(json_file)


def write_json(filename: str, data: dict) -> None:
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)


def read_binary(filename: str) -> bytes:
    with open(filename, "rb") as binary_file:
        return binary_file.read()


def write_binary(filename: str, data: bytes) -> None:
    with open(filename, "wb") as binary_file:
        binary_file.write(data)
