import requests
from PyQt5.QtGui import QPixmap
import logging
import urllib.parse

DEFAULT_TIMEOUT = 3


def is_valid_url(url: str) -> bool:
    """
    检查URL是否有效和安全。

    :param url: 待检查的URL字符串
    :return: 如果URL有效且安全，则返回True，否则返回False
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except ValueError:
        return False


def get_photo_from_internet(url: str) -> QPixmap | None:
    """
    从互联网获取照片。

    通过指定的URL尝试下载图片，并将其加载为QPixmap对象。
    如果下载或加载失败，则返回None。

    :param url: 图片的URL地址
    :return: 成功加载的图片对象，或在失败时返回None
    """
    if not is_valid_url(url):
        logging.warning("Invalid URL: %s", url)
        return None

    try:
        # 发起HTTP请求获取图片数据
        req = requests.get(url, timeout=DEFAULT_TIMEOUT)

        # 创建QPixmap对象并加载图片数据
        photo = QPixmap()
        photo.loadFromData(req.content)
        return photo
    except requests.exceptions.RequestException as e:
        # 记录请求异常到日志
        logging.error("Failed to download image from %s: %s", url, str(e))
    except Exception as e:
        # 记录其他异常到日志
        logging.error("Failed to process image from %s: %s", url, str(e))
    return None


if __name__ == "__main__":
    print(get_photo_from_internet("https://i0.hdslb.com/bfs/article/acbdf855c4d732ec9c84ed4e9719fd75188801893.jpg"))
