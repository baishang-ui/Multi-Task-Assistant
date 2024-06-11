import sys
from pathlib import Path

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QStyleOptionViewItem, QGridLayout
from qfluentwidgets import LineEdit, ExpandLayout, ElevatedCardWidget, ImageLabel, CaptionLabel, HeaderCardWidget, \
    BodyLabel, MSFluentTitleBar, isDarkTheme, TableItemDelegate, TableWidget
from PyQt5.QtGui import QColor, QPainterPath, QPainter, QPixmap
from qfluentwidgets import CardWidget
from PyQt5.QtCore import QEasingCurve, Qt, QModelIndex
from qfluentwidgets import FlowLayout
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel


class MLineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

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


class MCardWidget(CardWidget):
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
        self.descriptionLabel = BodyLabel(des, self)
        super().setBorderRadius(20)
        self.descriptionLabel.setWordWrap(False)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle(title)


class MImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        super().setBorderRadius(20, 20, 20, 20)


class MTable(QWidget):

    def __init__(self, title: list, data: list):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.tableView = TableWidget(self)

        # NOTE: use custom item delegate
        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        # select row on right-click
        # self.tableView.setSelectRightClickedRow(True)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(60)
        self.tableView.setColumnCount(5)
        dataInfos = data
        dataInfos += dataInfos
        for i, dataInfo in enumerate(dataInfos):
            for j in range(5):
                self.tableView.setItem(i, j, QTableWidgetItem(dataInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(title)
        self.tableView.resizeColumnsToContents()
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)

        self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.hBoxLayout.addWidget(self.tableView)
