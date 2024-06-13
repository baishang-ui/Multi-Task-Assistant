import os
import sys

from qfluentwidgets import PickerColumnFormatter


def time_to_seconds(d) -> int:
    d = list(map(int, d))
    res = d[0] * 3600 + d[1] * 60 + d[2]
    return res


def tenms_to_time(s):

    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return [h, m, s]


class SecondsFormatter(PickerColumnFormatter):
    """ Seconds formatter """

    def encode(self, value):
        return str(value) + "秒"

    def decode(self, value: str):
        return int(value[:-1])


class MinuteFormatter(PickerColumnFormatter):
    """ Seconds formatter """

    def encode(self, value):
        return str(value) + "分钟"

    def decode(self, value: str):
        return int(value[:-2])


class HoursFormatter(PickerColumnFormatter):
    """ Seconds formatter """

    def encode(self, value):
        return str(value) + "小时"

    def decode(self, value: str):
        return int(value[:-2])


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("")

    return os.path.normpath(os.path.join(base_path, relative_path))


def creat_file_dir():
    if not os.path.exists("Texture"):
        os.makedirs("Texture")


def safe_call(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except Exception as e:
        print(str(e))
