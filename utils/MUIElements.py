from pathlib import Path

from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve, QRect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from qfluentwidgets import CardWidget, SimpleCardWidget, setCustomStyleSheet, ComboBox, SearchLineEdit, \
    PrimaryPushButton, SmoothScrollArea
from qfluentwidgets import FlowLayout
from qfluentwidgets import FluentIcon as ficon
from qfluentwidgets import LineEdit, ExpandLayout, ElevatedCardWidget, ImageLabel, CaptionLabel, HeaderCardWidget, \
    BodyLabel


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
        super().setAnimation(500, QEasingCurve.InOutCubic)
        super().setContentsMargins(20, 20, 20, 20)
        super().setAlignment(Qt.AlignCenter)


class MQGridLayout(QGridLayout):
    def __init__(self, to):
        super().__init__(to)
        super().setContentsMargins(10, 10, 10, 10)


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
    def __init__(self, parent=None, candraw=True):
        super().__init__(parent=parent)
        super().setBorderRadius(14, 14, 14, 14)
        self.qr = None
        self.candraw = candraw
        self.start_point = None
        self.end_point = None
        self.start = False
        self.drawing = False
        if self.candraw:
            self.setCursor(Qt.CrossCursor)
            self.setMouseTracking(True)

    def paintEvent(self, event):
        super(MImageLabel, self).paintEvent(event)
        if self.drawing and self.candraw:
            painter = QPainter()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
            painter.begin(self)
            pen = QPen(Qt.white, 2)
            pen.setStyle(Qt.SolidLine)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            self.qr = QRect(self.start_point, self.end_point)
            painter.drawRect(self.qr)
            painter.end()

    def mousePressEvent(self, event):

        if not self.start:
            self.start_point = event.pos()
            self.start = True

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            self.start = False

    def mouseMoveEvent(self, event):
        if self.start and self.candraw:
            self.end_point = event.pos()
            self.drawing = True
            self.update()

    def get_qrect(self):
        return [self.qr.x(), self.qr.y(), self.qr.x() + self.qr.width(), self.qr.y() + self.qr.height()]


class MPushButton(PrimaryPushButton):

    def __init__(self, text=None, icon=ficon.CHECKBOX, parent=None):
        super().__init__(parent=parent)
        self.qss = 'PrimaryPushButton{border-radius: 10px}'
        setCustomStyleSheet(self, self.qss, self.qss)
        self.setText(text)
        self.setIcon(icon)


class MSmoothScrollArea(SmoothScrollArea):

    def __init__(self, ele):
        super().__init__()
        self.setScrollAnimation(Qt.Vertical, 700, QEasingCurve.OutCubic)
        self.setScrollAnimation(Qt.Horizontal, 700, QEasingCurve.OutCubic)
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
        ele.setStyleSheet("QWidget{background: transparent}")
        self.setWidget(ele)
