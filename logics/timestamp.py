from repositories.system import exists_path, read_json
from configs import TIMESTAMP_FILENAME
from schemas import GetLatestUpdateDateReturnValue


def get_latest(user_name: str) -> GetLatestUpdateDateReturnValue:
    if not exists_path(TIMESTAMP_FILENAME):
        return GetLatestUpdateDateReturnValue(
            date=None
        )

    user_data = read_json(TIMESTAMP_FILENAME)
    date = user_data.get(user_name, None)
    return GetLatestUpdateDateReturnValue(date=date)
