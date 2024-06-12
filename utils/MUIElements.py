from pathlib import Path

from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QGridLayout, QGraphicsBlurEffect, \
    QPushButton
from qfluentwidgets import CardWidget, SimpleCardWidget, PushButton, setCustomStyleSheet, ComboBox, SearchLineEdit
from qfluentwidgets import FlowLayout
from qfluentwidgets import LineEdit, ExpandLayout, ElevatedCardWidget, ImageLabel, CaptionLabel, HeaderCardWidget, \
    BodyLabel, TableWidget
from qfluentwidgets.common.animation import DropShadowAnimation


class MLineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.qss = 'LineEdit{border-radius: 10px}'
        setCustomStyleSheet(self, self.qss, self.qss)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        # 拖拽多文件只取第一个地址
        filePath = filePathList.split('\n')[0]
        # 去除文件地址前缀的特定字符
        filePath = filePath.replace('file:///', '', 1)
        self.setText(filePath)


class MComboBox(ComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qss = 'ComboBox{border-radius: 10px}'
        setCustomStyleSheet(self, self.qss, self.qss)


class MSearchLineEdit(SearchLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qss = 'LineEdit{border-radius: 10px}'
        setCustomStyleSheet(self, self.qss, self.qss)


class MCardWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        super().setBorderRadius(20)


class MSimpleCardWidget(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        super().setBorderRadius(20)


class MFLayout(FlowLayout):
    def __init__(self, to):
        super().__init__(to, needAni=True)
        super().setAnimation(350, QEasingCurve.OutQuad)
        super().setContentsMargins(20, 20, 20, 20)
        super().setAlignment(Qt.AlignCenter)


class MQGridLayout(QGridLayout):
    def __init__(self, to):
        super().__init__(to)
        super().setContentsMargins(20, 20, 20, 20)


class MExpandLayout(ExpandLayout):
    def __init__(self, to):
        super().__init__(to)
        super().setContentsMargins(20, 0, 20, 20)


class MAnimation(QPropertyAnimation):
    def __init__(self, obj, e, start, end, duration, easing=QEasingCurve.InOutCubic, parent=None):
        super().__init__(obj, e, parent=parent)
        super().setDuration(duration)
        super().setStartValue(start)
        super().setEndValue(end)
        super().setEasingCurve(easing)

    def start_animation(self):
        super().start(QAbstractAnimation.DeleteWhenStopped)


class MImageCard(ElevatedCardWidget):
    """ Emoji card """

    def __init__(self, imagePath: str, parent=None):
        super().__init__(parent)
        self.iconWidget = ImageLabel(imagePath, self)
        self.label = CaptionLabel(Path(imagePath).stem, self)

        self.iconWidget.scaledToHeight(68)
        self.iconWidget.setBorderRadius(10, 10, 10, 10)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(
            self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(168, 176)


class MDescriptionCard(HeaderCardWidget):

    def __init__(self, title="描述", des="", parent=None):
        super().__init__(parent)
        super().setBorderRadius(20)
        self.descriptionLabel = BodyLabel(des, self)
        self.descriptionLabel.setWordWrap(False)
        self.viewLayout.setAlignment(Qt.AlignCenter)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle(title)

    def setDes(self, des):
        self.descriptionLabel.setText(des)


class MImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        super().setBorderRadius(14, 14, 14, 14)


class MPushButton(PushButton):

    def __init__(self, text=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.qss = 'PushButton{border-radius: 10px}'
        setCustomStyleSheet(self, self.qss, self.qss)
