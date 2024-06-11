import requests
from PyQt5.QtGui import QPixmap


def get_photo_from_internet(url: str) -> QPixmap:
    random_pic = url
    try:
        req = requests.get(random_pic, timeout=3)
        photo = QPixmap()
        photo.loadFromData(req.content)
        return photo
    except Exception as e:
        return None


if __name__ == "__main__":
    print(get_photo_from_internet("https://i0.hdslb.com/bfs/article/acbdf855c4d732ec9c84ed4e9719fd75188801893.jpg"))
