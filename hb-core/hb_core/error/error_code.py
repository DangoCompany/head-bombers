from enum import IntEnum


class ErrorCode(IntEnum):
    FILE_NOT_EXIST = 1
    INVALID_IMAGE_FORMAT = 2
    NO_VALID_OBJECT_CLASS_DETECTED = 3
