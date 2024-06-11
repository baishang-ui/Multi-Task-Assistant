# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, \
    QTableWidgetItem

from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon, TableWidget


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


class Demo(QWidget):

    def __init__(self,data):
        super().__init__()
        # setTheme(Theme.DARK)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.table_qw = []
        for i in range(len(data)):
            ele = data[i][0]
            qw = MTable(['1', '2', '3', '4', '5'],[['かばん', 'aiko', 'かばん', '2004', '5:04'],])
            self.table_qw.append(qw)
            # add items to pivot
            self.addSubInterface(self.table_qw[i], ele+"interface", ele)

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.table_qw[0])
        self.pivot.setCurrentItem(self.table_qw[0].objectName())

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo([('上海', '阴', '-', '21'), ('闵行', '阴', '-', '20')])
    w.show()
    app.exec_()
