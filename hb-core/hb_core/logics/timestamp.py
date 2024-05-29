from configs import TIMESTAMP_FILENAME
from hb_core.dtos.dto import GetLatestUpdateDateReturnValue
from hb_core.repositories.system import exists_path, read_json


def get_latest(user_name: str) -> GetLatestUpdateDateReturnValue:
    if not exists_path(TIMESTAMP_FILENAME):
        return GetLatestUpdateDateReturnValue(error_codes=(), date=None)

    user_data = read_json(TIMESTAMP_FILENAME)
    date = user_data.get(user_name, None)
    return GetLatestUpdateDateReturnValue(error_codes=(), date=date)
