from enum import Enum


class InputFormat(str, Enum):
    data = "data"
    csv = "csv"


INPUT_FORMATS = InputFormat
