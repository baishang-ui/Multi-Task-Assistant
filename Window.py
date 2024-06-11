# coding:utf-8
import os

from PIL import Image, ImageFilter
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QPoint, QTime, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices, QFont
from PyQt5.QtWidgets import QApplication, QCompleter
from qfluentwidgets import FluentIcon as ficon, PixmapLabel, Slider, FlyoutView, Flyout, FlyoutAnimationType, \
    TimePicker, ProgressRing, SearchLineEdit
from qfluentwidgets import (NavigationItemPosition, MessageBox,
                            MSFluentWindow, AvatarWidget, InfoBar, InfoBarPosition,
                            PushButton, ComboBox, Theme, setTheme, setThemeColor)

import Utils
from GetPhotoFromInternet import get_photo_from_internet
from GetWeather import get_weather_data
from MUIElements import *


class Widget(QWidget):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        setTheme(Theme.DARK)
        setThemeColor("#b9beed")
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    def __init__(self):
        super().__init__()
        # create sub interface

        self.layout_app_card2 = None
        self.app_card2 = None
        self.card1_info_card4 = None
        self.card1_info_card3 = None
        self.card1_info_card2 = None
        self.card1_info_card1 = None
        self.layout_home_card1_ava_card3 = None
        self.layout_home_card1_ava_card2 = None
        self.layout_home_card1_ava_card4 = None
        self.card1_ava_card4 = None
        self.card1_ava_card3 = None
        self.card1_ava_card2 = None
        self.ava4 = None
        self.ava3 = None
        self.ava2 = None
        self.ava1 = None
        self.weather_position = ""
        self.card2_weather_card_label1 = None
        self.weather_data = {}
        self.home_weather_card_combobox = None
        self.resource_ava = utils.get_path("resource/ava.png")
        self.resource_logo = utils.get_path("resource/logo.png")
        self.resource_home_p = utils.get_path("resource/home.png")
        self.calc_time = 300
        self.system_timer = None
        self.layout_app_card1 = None
        self.timePicker = None
        self.timer_start_button = None
        self.timer_label1 = None
        self.timer_label2 = None
        self.current_time = None
        self.app_card1 = None
        self.progress_circle = None
        self.time_count = 0
        self.timer_start_button_flag = True
        self.extend_card2_tip = None
        self.layout_home_card1 = None
        self.layout_card3 = None
        self.home_card3 = None
        self.layout_home_card1_ava_card1 = None
        self.card1_ava_card1 = None
        self.home_card1 = None
        self.ava = None
        self.layout_home_card2 = None
        self.home_card2 = None
        self.home_photo_show = None
        if not os.path.exists("Texture"):
            os.makedirs("Texture")
        self.current_dir = os.getcwd() + "\\Texture\\"
        self.extend_slider_value = 0.0
        self.extend_slider = None
        self.extend_combobox = None
        self.pixmap_type = "旋转"
        self.extend_card1_layout = None
        self.extend_start_button = None
        self.extend_card1 = None
        self.extend_card2_layout = None
        self.extend_card2 = None
        self.pix = QPixmap(self.resource_ava)
        self.Font = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.pixmap = None
        self.file_dir = ""
        self.extend_drag_edit = None
        self.layout_home_card2_weather_card = None
        self.card2_weather_card_label3 = None
        self.card2_weather_card_label4 = None
        self.card2_weather_card = None
        self.card2_weather_card_label2 = None
        self.home_card2 = None
        self.layout_home_card2 = None
        self.start_animation_alpha = None
        self.start_animation_pos = None
        self.homeInterface = Widget('home', self)
        self.appInterface = Widget('app', self)
        self.extendInterface = Widget('extend', self)

        self.initWindow()
        self.initNavigation()
        self.initHomeInterface()
        self.initAppInterface()
        self.initExtendInterface()

    def show_message_box(self):
        w = MessageBox(
            '信息',
            'By BaiShang',
            self
        )
        w.yesButton.setText('1')
        w.cancelButton.setText('2')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://space.bilibili.com/188801893?spm_id_from=333.1007.0.0"))

    def show_info_bar(self, content="消息", typ="new", title="", duration=1500):
        match typ:
            case "success":
                InfoBar.success(
                    title=title,
                    content=content,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=duration,
                    parent=self
                )
            case "warning":
                InfoBar.warning(
                    title=title,
                    content=content,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=duration,
                    parent=self
                )
            case "error":
                InfoBar.error(
                    title=title,
                    content=content,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=duration,
                    parent=self
                )
            case "new":
                w = InfoBar.new(
                    icon=ficon.HOME,
                    title=title,
                    content=content,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=duration,
                    parent=self
                )
                w.setCustomBackgroundColor('white', '#202020')

    def show_flyout_view(self):
        view = FlyoutView(
            title='BaiShang',
            content="MAVERICK",
            image=self.resource_ava,
            isClosable=True
            # image='resource/yiku.gif',
        )

        # add button to view

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 15)
        view.widgetLayout.addSpacing(11)

        # show view
        w = Flyout.make(view, self.card1_ava_card1, self, aniType=FlyoutAnimationType.SLIDE_RIGHT)
        view.closed.connect(w.close)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, ficon.HOME, '主页', ficon.HOME_FILL)
        self.addSubInterface(self.appInterface, ficon.DATE_TIME, '时钟')
        self.addSubInterface(self.extendInterface, ficon.PHOTO, '图片处理')

        # 添加自定义导航组件
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=ficon.HELP,
            text='帮助',
            onClick=self.show_message_box,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1077, 761)
        self.setWindowIcon(QIcon(self.resource_logo))
        self.setWindowTitle('Main Window')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.start_animation_pos = MAnimation(self, b'pos', QPoint(w // 2 - self.width() // 2, h + 46),
                                              QPoint(w // 2 - self.width() // 2, h // 2 - self.height() // 2),
                                              1100)
        self.start_animation_pos.start()
        self.start_animation_alpha = MAnimation(self, b'windowOpacity', 0, 1, 500)
        self.start_animation_alpha.start()

    def initHomeInterface(self):

        layout = MQGridLayout(self.homeInterface)
        # 创建第一个大卡片存放信息卡片
        self.home_card1 = MCardWidget(self.homeInterface)
        self.layout_home_card1 = MQGridLayout(self.home_card1)
       # self.layout_home_card1.setAlignment(Qt.AlignCenter)
        # 设置头像卡片的布局
        self.ava1 = AvatarWidget(
            get_photo_from_internet("https://i0.hdslb.com/bfs/article/acbdf855c4d732ec9c84ed4e9719fd75188801893.jpg"))
        self.card1_ava_card1 = MCardWidget()
        self.layout_home_card1_ava_card1 = MQGridLayout(self.card1_ava_card1)
        self.layout_home_card1_ava_card1.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card1.addWidget(self.ava1)

        self.ava2 = AvatarWidget(
            get_photo_from_internet("https://i0.hdslb.com/bfs/article/f6e5c5a71e735d0affe2e1550c89e922188801893.jpg"))
        self.card1_ava_card2 = MCardWidget()
        self.layout_home_card1_ava_card2 = MQGridLayout(self.card1_ava_card2)
        self.layout_home_card1_ava_card2.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card2.addWidget(self.ava2)

        self.ava3 = AvatarWidget(
            get_photo_from_internet("https://i0.hdslb.com/bfs/article/a59d70a80efe44a6c5ca17e8e4d34375188801893.jpg"))
        self.card1_ava_card3 = MCardWidget()
        self.layout_home_card1_ava_card3 = MQGridLayout(self.card1_ava_card3)
        self.layout_home_card1_ava_card3.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card3.addWidget(self.ava3)

        self.ava4 = AvatarWidget(
            get_photo_from_internet("https://i0.hdslb.com/bfs/article/3474819e8223a34e7b525be138a74cc8188801893.jpg"))
        self.card1_ava_card4 = MCardWidget()
        self.layout_home_card1_ava_card4 = MQGridLayout(self.card1_ava_card4)
        self.layout_home_card1_ava_card4.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card4.addWidget(self.ava4)

        self.card1_ava_card1.clicked.connect(self.show_flyout_view)

        self.card1_info_card1 = MDescriptionCard("成员", "202209160316-毕天宇")
        self.card1_info_card2 = MDescriptionCard("成员", "202209160307-赵锐")
        self.card1_info_card3 = MDescriptionCard("成员", "202209160305-陈影茜")
        self.card1_info_card4 = MDescriptionCard("成员", "202209160301-魏艳")
        # 将头像卡片添加到第一个大卡片
        # 1
        self.layout_home_card1.addWidget(self.card1_ava_card1, 0, 0)
        self.layout_home_card1.addWidget(self.card1_info_card1, 1, 0)
        # 2
        self.layout_home_card1.addWidget(self.card1_ava_card2, 0, 1)
        self.layout_home_card1.addWidget(self.card1_info_card2, 1, 1)
        # 3
        self.layout_home_card1.addWidget(self.card1_ava_card3, 0, 2)
        self.layout_home_card1.addWidget(self.card1_info_card3, 1, 2)
        # 4
        self.layout_home_card1.addWidget(self.card1_ava_card4, 0, 3)
        self.layout_home_card1.addWidget(self.card1_info_card4, 1, 3)

        # 创建第二个大卡片存放天气卡片
        self.home_card2 = MCardWidget()
        self.layout_home_card2 = MQGridLayout(self.home_card2)
        self.home_card2.clicked.connect(lambda: print(self.width(),self.height()))

        # 获取临沂天气
        all_weather = get_weather_data()
        self.weather_data = {}
        stands = []
        for i in range(len(all_weather)):
            self.weather_data[all_weather[i][0]] = (all_weather[i][1:])
            stands.append(all_weather[i][0])
        self.home_weather_card_combobox = SearchLineEdit()
        completer = QCompleter(stands, self.home_weather_card_combobox)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        self.home_weather_card_combobox.setCompleter(completer)
        self.home_weather_card_combobox.textChanged.connect(self.weather_position_get)
        # 创建天气卡片基于第二个大卡片
        self.card2_weather_card = MCardWidget()

        # 设置天气卡片的布局
        self.layout_home_card2_weather_card = MFLayout(self.card2_weather_card)

        # 添加地名到天气卡片
        self.card2_weather_card_label1 = MDescriptionCard("🟡城市名称", "未选择")
        self.layout_home_card2_weather_card.addWidget(self.card2_weather_card_label1)
        # 添加天气到天气卡片
        self.card2_weather_card_label2 = MDescriptionCard("🟡天气状况", "未找到")
        self.layout_home_card2_weather_card.addWidget(self.card2_weather_card_label2)

        # 添加最高温到天气卡片
        self.card2_weather_card_label3 = MDescriptionCard("🟡最高气温", "未找到")
        self.layout_home_card2_weather_card.addWidget(self.card2_weather_card_label3)


        # 添加最低温到天气卡片
        self.card2_weather_card_label4 = MDescriptionCard("🟡最低气温", "未找到")
        self.layout_home_card2_weather_card.addWidget(self.card2_weather_card_label4)
        # 添加天气卡片到第二个大卡片
        self.layout_home_card2.addWidget(self.home_weather_card_combobox)
        self.layout_home_card2.addWidget(self.card2_weather_card)

        # 创建第三个大卡片存放图片卡片一言卡片
        self.home_card3 = MCardWidget()
        self.layout_card3 = MFLayout(self.home_card3)
        qpix = 1  # get_photo_from_internet("https://t.alcy.cc/fj/")
        image_label = MImageLabel()
        image_label.setImage(self.resource_home_p)
        image_label.scaledToWidth(580)

        # 添加图片卡片到第三个大卡片
        self.layout_card3.addWidget(image_label)
        # 添加三个到主页面
        layout.addWidget(self.home_card3, 0, 0, 1, 1)
        layout.addWidget(self.home_card2, 0, 1, 1, 1)
        layout.addWidget(self.home_card1, 1, 0, 1, 2)

    def initAppInterface(self):
        layout = MQGridLayout(self.appInterface)
        layout.setAlignment(Qt.AlignTop)
        self.system_timer = QtCore.QTimer()
        self.system_timer = QTimer(self.appInterface, timeout=self.run_timer)

        self.app_card1 = MCardWidget()
        self.layout_app_card1 = MQGridLayout(self.app_card1)
        self.layout_app_card1.setAlignment(Qt.AlignTop)

        self.app_card2 = MCardWidget()
        self.layout_app_card2 = MQGridLayout(self.app_card2)
        self.layout_app_card2.setAlignment(Qt.AlignCenter)

        self.timePicker = TimePicker(None, True)
        self.timePicker.setColumnFormatter(0, utils.HoursFormatter())
        self.timePicker.setColumnFormatter(1, utils.MinuteFormatter())
        self.timePicker.setColumnFormatter(2, utils.SecondsFormatter())
        self.current_time = QTime().currentTime()

        self.progress_circle = ProgressRing()
        # 设置进度环取值范围和当前值
        self.progress_circle.setRange(0, 100)

        # 显示进度环内文本
        self.progress_circle.setTextVisible(True)

        # 调整进度环大小
        self.progress_circle.setFixedSize(80, 80)

        # 调整厚度
        self.progress_circle.setStrokeWidth(14)

        # 时间发生改变
        self.timePicker.timeChanged.connect(lambda time: self.get_calc_time(time.toString()))
        self.timer_start_button = PushButton("开始计时", self.app_card1)
        self.timer_label1 = BodyLabel("定时时间选择:")
        self.timer_start_button.clicked.connect(self.timer_button_action)
        self.layout_app_card1.addWidget(self.timer_label1, 1, 0)
        self.layout_app_card1.addWidget(self.timePicker, 1, 1)
        self.layout_app_card1.addWidget(self.timer_start_button, 1, 2)
        self.layout_app_card2.addWidget(self.progress_circle, 2, 2)

        layout.addWidget(self.app_card1, 0, 0)
        layout.addWidget(self.app_card2, 0, 1)

    def initExtendInterface(self):
        layout = MQGridLayout(self.extendInterface)
        layout.setAlignment(Qt.AlignTop)
        self.extend_card1 = MCardWidget()
        self.extend_card1_layout = MFLayout(self.extend_card1)
        self.extend_drag_edit = MLineEdit()
        self.extend_drag_edit.setFixedSize(200, 32)
        self.extend_drag_edit.setPlaceholderText("拖拽到此或者输入路径")
        self.extend_drag_edit.setClearButtonEnabled(True)
        self.extend_card1_layout.addWidget(self.extend_drag_edit)

        self.extend_start_button = PushButton()
        self.extend_start_button.setText("开始")
        self.extend_card1_layout.addWidget(self.extend_start_button)
        self.extend_combobox = ComboBox()
        items = ['旋转', '缩小', '模糊', '轮廓', "平滑", "锐化", "边界", "边界加强", "浮雕", "细节"]
        self.extend_combobox.addItems(items)
        self.extend_combobox.currentIndexChanged.connect(self.pixmap_get_type)
        self.extend_card1_layout.insertWidget(1, self.extend_combobox)
        self.extend_slider = Slider(Qt.Horizontal)
        self.extend_slider.setFixedWidth(200)
        self.extend_slider.valueChanged.connect(self.extend_get_slider)
        self.extend_card1_layout.addWidget(self.extend_slider)

        self.extend_card2 = MCardWidget()
        self.extend_card2_layout = MFLayout(self.extend_card2)
        self.extend_card2_tip = BodyLabel()
        self.extend_card2_tip.setText("图片预览")
        self.extend_card2_layout.addWidget(self.extend_card2_tip)
        self.pixmap = PixmapLabel()
        self.extend_drag_edit.textChanged.connect(self.file_dir_get)
        self.extend_start_button.clicked.connect(self.handle_pixmap)
        layout.addWidget(self.extend_card1, 0, 0)
        layout.addWidget(self.extend_card2, 0, 1)

    def get_calc_time(self, time: str):
        try:
            time = time.split(":")
            self.calc_time = utils.time_to_seconds(time)
        except Exception as e:
            print(e)

    def timer_button_action(self):
        self.timer_start_button_flag = not self.timer_start_button_flag

        if self.timer_start_button_flag:
            self.timer_start_button.setText("开始计时")
            try:
                self.time_count = 0
                self.progress_circle.setValue(0)
                self.system_timer.stop()
            except Exception as e:
                print(e)
        else:
            self.timer_start_button.setText("关闭计时")
            try:
                self.system_timer.start(1000)
            except Exception as e:
                print(e)

    def run_timer(self):
        self.time_count += 1
        try:
            percent = int((self.time_count / self.calc_time) * 100)
            if percent > 100:
                self.timer_button_action()
                self.show_info_bar("计时完成", "success", "计时器")
            else:
                self.progress_circle.setValue(percent)
        except Exception as e:
            print(e)

    def file_dir_get(self):
        res = self.extend_drag_edit.text()
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.file_dir = self.extend_drag_edit.text()
        if len(res.split("/")) > 2:
            try:
                self.extend_card2_layout.removeWidget(self.pixmap)
                self.pix = QPixmap(self.file_dir)
                pixh = self.pix.height()
                pixw = self.pix.width()
                l = pixh / 300
                r = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(r), 300))
                self.extend_card2_layout.addWidget(self.pixmap)
                self.extend_card2.setFixedSize(int(r) + 40, 380)
            except Exception as e:
                print(e)

    def handle_pixmap(self):
        if self.file_dir == "":
            self.show_info_bar("路径为空", "error", "错误")
        else:
            try:
                new_file = ""
                to = self.file_dir.split("/")
                pit_name = to[-1]
                im = Image.open(self.file_dir)
                slider_value = self.extend_slider_value
                match self.pixmap_type:
                    case "旋转":
                        handled = im.rotate(int(slider_value * 360))
                        fix_name = f"rotate({str(int(slider_value * 360))})+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "缩小":
                        q = slider_value == 0 and 0.1 or slider_value
                        tup = (int(im.size[0] * q), int(im.size[1] * q))
                        handled = im.resize(tup)
                        fix_name = f"resize({str(tup)})+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "模糊":
                        handled = im.filter(ImageFilter.GaussianBlur(int(slider_value * 100)))
                        fix_name = f"blur({int(slider_value * 100)})+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "轮廓":
                        handled = im.filter(ImageFilter.CONTOUR)
                        fix_name = f"contour+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "平滑":
                        handled = im.filter(ImageFilter.SMOOTH_MORE)
                        fix_name = f"smooth+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "锐化":
                        handled = im.filter(ImageFilter.SHARPEN)
                        fix_name = f"sharpen+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "边界":
                        handled = im.filter(ImageFilter.FIND_EDGES)
                        fix_name = f"find_edges+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "边界加强":
                        handled = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
                        fix_name = f"edge_enhance+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "浮雕":
                        handled = im.filter(ImageFilter.EMBOSS)
                        fix_name = f"emboss+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                    case "细节":
                        handled = im.filter(ImageFilter.DETAIL)
                        fix_name = f"detail+{pit_name}"
                        new_file = self.current_dir + "/" + fix_name
                        handled.save(new_file)
                self.extend_card2_layout.removeWidget(self.pixmap)
                self.pix = QPixmap(new_file)
                pixh = self.pix.height()
                pixw = self.pix.width()
                l = pixh / 300
                r = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(r), 300))
                self.extend_card2_layout.addWidget(self.pixmap)
                self.extend_card2.setFixedSize(int(r) + 40, 380)

            except Exception as e:
                self.show_info_bar(str(e))

    def pixmap_get_type(self):
        res = self.extend_combobox.currentText()
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        if res != "旋转" and res != "缩小" and res != "模糊":
            self.extend_slider.hide()
        else:
            self.extend_slider.show()
        self.pixmap_type = res

    def weather_position_get(self):
        res = self.home_weather_card_combobox.text()
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.weather_position = res

        if len(self.weather_position) == 0:
            return
        if '\u4e00' <= self.weather_position[0] <= '\u9fff':
            try:
                self.card2_weather_card_label1.setDes(self.weather_position)
                self.card2_weather_card_label2.setDes(self.weather_data[res][0])
                self.card2_weather_card_label3.setDes(
                    self.weather_data[res][1] == '-' and "🟡当前时段" or "🟡最高气温")
                self.card2_weather_card_label3.setDes(
                    self.weather_data[res][1] == '-' and "夜间" or self.weather_data[res][1])
                self.card2_weather_card_label4.setDes(self.weather_data[res][2])
            except Exception as e:
                self.card2_weather_card_label1.setDes("未选择")
                self.card2_weather_card_label2.setDes("未找到")
                self.card2_weather_card_label3.setDes("未找到")
                self.card2_weather_card_label4.setDes("未找到")

    def extend_get_slider(self):
        res = self.extend_slider.value() / 100
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.extend_slider_value = res


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
