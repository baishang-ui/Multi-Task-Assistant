import requests
from PyQt5.QtGui import QPixmap


def get_photo_from_internet(url: str) -> QPixmap:
    random_pic = url
    try:
        req = requests.get(random_pic)
        photo = QPixmap()
        photo.loadFromData(req.content)
        return photo
    except Exception as e:
        print(e)


if __name__ == "__main__":
    get_photo_from_internet()
