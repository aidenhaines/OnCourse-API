from typing import Union
import datetime


def timestamp_converter(value: Union[int, float, str]) -> datetime.datetime:
    if isinstance(value, str):
        return datetime.datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
    elif isinstance(value, (float, int)):
        return datetime.datetime.fromtimestamp(float(value))
    raise TypeError("Timestamp must be one of: datetime, int, float, ISO8601 str")
