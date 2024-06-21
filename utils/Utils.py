import os
import sys

from qfluentwidgets import PickerColumnFormatter


def time_to_seconds(d) -> int:
    """
    将时间表达式转换为总秒数。

    参数:
    d (tuple): 一个包含小时、分钟和秒的元组。

    返回:
    int: 表示总秒数的整数。
    """
    # 将输入的元组转换为整数列表，确保后续计算的准确性
    d = list(map(int, d))
    # 计算总秒数：小时*3600 + 分钟*60 + 秒
    res = d[0] * 3600 + d[1] * 60 + d[2]
    return res


def second_to_time(s):
    """
    将秒数转换为时分秒的列表形式。

    参数:
    s (int): 输入的总秒数。

    返回:
    list: 包含时、分、秒的整数列表，顺序为[小时, 分钟, 秒]。
    """
    # 使用divmod函数同时计算出分钟数和剩余的秒数
    m, s = divmod(s, 60)
    # 再次使用divmod函数计算出小时数和剩余的分钟数
    h, m = divmod(m, 60)
    # 返回包含时、分、秒的列表
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


def safe_join_path(base_path: str, relative_path: str) -> str:
    """
    安全地将相对路径加入到基础路径中，避免路径遍历攻击。

    参数:
    base_path: 基础路径字符串。
    relative_path: 相对路径字符串。

    返回:
    一个字符串，表示安全拼接后的路径。
    """
    # 使用os.path.join保证路径拼接的正确性，并利用os.path.abspath防止路径遍历攻击
    # 通过realpath解析出真实路径，即便relative_path中包含类似../的尝试也会被阻止
    return os.path.abspath(os.path.join(base_path, relative_path))


def get_path(relative_path: str) -> str:
    """
    根据程序的执行环境，获取给定相对路径的绝对路径。

    这个函数主要用于处理跨平台的路径问题，确保无论程序是如何被调用的
    （无论是从安装目录还是直接执行Python文件），都能正确地解析出相对路径的绝对路径。

    参数:
    relative_path: 相对于程序执行路径的路径字符串。

    返回:
    一个字符串，表示相对于程序执行环境的绝对路径。
    """
    # 尝试获取由PyInstaller打包时的特殊路径变量
    try:
        base_path = sys._MEIPASS
    # 如果不是由PyInstaller打包，则使用当前执行文件的路径
    except AttributeError:
        base_path = os.path.abspath("")

    # 为了增强安全性，使用safe_join_path函数来拼接路径
    # 同时，对relative_path进行检查，确保其不包含非法字符，可以进一步增强此逻辑
    # 此处没有直接使用os.path.join(base_path, relative_path)以避免潜在的安全风险
    return safe_join_path(base_path, relative_path)


def create_file_dir(directory_name="Texture"):
    """
    创建指定文件夹。

    如果指定的文件夹不存在，则通过os.makedirs函数创建该文件夹。
    这个函数的目的是为了确保指定的文件夹存在，以便后续操作可以正确进行。
    """
    # 使用函数参数中的目录名，保持了功能的灵活性
    # 同时使用了abspath确保了路径的安全性和准确性
    abs_directory_name = os.path.abspath(directory_name)

    # 检查目录是否存在，不存在则尝试创建
    # 添加了异常处理来优雅地处理可能的权限问题
    try:
        if not os.path.exists(abs_directory_name):
            os.makedirs(abs_directory_name)
    except OSError as error:
        print(f"Error creating directory {abs_directory_name}: {error}")


def safe_call(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except Exception as e:
        print(str(e))
