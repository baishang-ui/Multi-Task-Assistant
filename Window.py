# coding:utf-8
import os
import sys
from PIL import Image, ImageFilter
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QPoint, QTime, QTimer, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QFont
from PyQt5.QtWidgets import QApplication, QCompleter, QWidget
from qfluentwidgets import FlyoutView, Flyout, FlyoutAnimationType, \
    TimePicker, ProgressRing, Slider, SwitchButton, ProgressBar, StrongBodyLabel, \
    SubtitleLabel
from qfluentwidgets import (NavigationItemPosition, MessageBox,
                            MSFluentWindow, AvatarWidget, InfoBar, InfoBarPosition,
                            Theme, setTheme, setThemeColor)

from utils import Utils
from utils.GetPhotoFromInternet import *
from utils.GetWeather import *
from utils.MUIElements import *


class Widget(QWidget):
    """
    Widget类继承自Qwidget，用于创建带有特定文本标签的界面元素。

    参数:
    - text: str，界面元素的文本标签。
    - parent: QWidget，父窗口对象，默认为None。
    """

    def __init__(self, text: str, parent=None):
        """
        初始化Widget对象。

        设置对象名，基于传入的文本参数，将空格替换为连字符，以符合对象名的命名规则。
        """
        super().__init__(parent=parent)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    def __init__(self):
        super().__init__()

        self.splashScreen = None
        self.home_b_photo = None
        self.splash = None
        self.desktop = QApplication.desktop().availableGeometry()
        self.pc_w, self.pc_h = self.desktop.width(), self.desktop.height()
        self.progress_circle_countdown = None
        self.countdown_pause_button = None
        self.countdown_label = SubtitleLabel()
        self.countdown_start_button = MPushButton()
        self.countdown_pause_flag = False
        self.system_count_down = QTimer()
        self._extend_layout = MQGridLayout(None)
        self.home_weather_re_get_button = MPushButton()
        self.extend_slider_label = BodyLabel()
        setTheme(Theme.AUTO)
        setThemeColor("#b9beed")
        self.pic_h = 300
        self.pic_w = 0
        self.all_weather = None
        self.weather_state = False
        self.layout_app_card2 = MQGridLayout(None)
        self.app_card2 = MSimpleCardWidget()
        self.card1_info_card4 = MDescriptionCard()
        self.card1_info_card3 = MDescriptionCard()
        self.card1_info_card2 = MDescriptionCard()
        self.card1_info_card1 = MDescriptionCard()
        self.layout_home_card1_ava_card3 = MQGridLayout(None)
        self.layout_home_card1_ava_card2 = MQGridLayout(None)
        self.layout_home_card1_ava_card4 = MQGridLayout(None)
        self.card1_ava_card4 = MCardWidget()
        self.card1_ava_card3 = MCardWidget()
        self.card1_ava_card2 = MCardWidget()
        self.ava4 = AvatarWidget()
        self.ava3 = AvatarWidget()
        self.ava2 = AvatarWidget()
        self.ava1 = AvatarWidget()
        self.weather_position = ""
        self.card2_weather_card_label1 = MDescriptionCard()
        self.weather_data = {}
        self.home_weather_card_combobox = None
        self.resource_ava = Utils.get_path("resource/ava.png")
        self.city_code = Utils.get_path("resource/city_to_code.json")
        self.resource_logo = Utils.get_path("resource/logo.png")
        self.resource_home_p = Utils.get_path("resource/home.png")
        self.resource_gif1 = Utils.get_path("resource/1.gif")
        self.a1 = QPixmap(self.resource_ava)
        self.a2 = QPixmap(self.resource_ava)
        self.a3 = QPixmap(self.resource_ava)
        self.a4 = QPixmap(self.resource_ava)
        self.calc_time = 300
        self.system_timer = None
        self.layout_app_card1 = None
        self.timePicker = None
        self.timer_start_button = SwitchButton()
        self.timer_label1 = None
        self.timer_label2 = None
        self.current_time = None
        self.app_card1 = None
        self.progress_circle_timer = None
        self.time_count = 0
        self.countdown_count = 0
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
        Utils.create_file_dir()
        self.current_dir = os.getcwd() + "\\Texture\\"
        self.extend_slider_value = 0.0
        self.extend_slider = Slider(None)
        self.extend_combobox = MComboBox()
        self.pixmap_type = "旋转"
        self.extend_card1_layout = MFLayout(None)
        self.extend_start_button = MPushButton()
        self.extend_card1 = MSimpleCardWidget()
        self.extend_card2_layout = MFLayout(None)
        self.extend_card2 = MSimpleCardWidget()
        self.pix = QPixmap(self.resource_ava)
        self.Font = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.pixmap = None
        self.file_dir = ""
        self.extend_drag_edit = MLineEdit()
        self.card2_weather_card_label3 = MDescriptionCard()
        self.card2_weather_card_label4 = MDescriptionCard()
        self.card2_weather_card_label2 = MDescriptionCard()
        self.home_card2 = None
        self.layout_home_card2 = None
        self.start_animation_alpha = None
        self.start_animation_pos = None
        self.homeInterface = Widget('home', self)
        self.appInterface = Widget('app', self)
        self.extendInterface = Widget('extend', self)

        self.initWindow()
        self.get_internet_data()
        self.initHomeInterface()
        self.initAppInterface()
        self.initExtendInterface()
        self.initNavigation()
        self.splashScreen.finish()
        self.start_animation_pos = MAnimation(self, b'pos', QPoint(self.pc_w // 2 - self.width() // 2, self.pc_h + 46),
                                              QPoint(self.pc_w // 2 - self.width() // 2,
                                                     self.pc_h // 2 - self.height() // 2),
                                              1100)
        self.start_animation_pos.start()
        self.start_animation_alpha = MAnimation(self, b'windowOpacity', 0, 1, 500)
        self.start_animation_alpha.start()

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
        self.resize(977, 685)
        self.setWindowIcon(QIcon(self.resource_logo))
        self.setWindowTitle('Main Window')
        self.desktop = QApplication.desktop().availableGeometry()
        self.move(self.pc_w // 2 - self.width() // 2, self.pc_h // 2 - self.height() // 2)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

    def get_internet_data(self):
        QApplication.processEvents()
        self.a1 = get_photo_from_internet("https://i0.hdslb.com/bfs/article/acbdf855c4d732ec9c84ed4e9719fd75188801893"
                                          ".jpg")

        self.a2 = get_photo_from_internet("https://i0.hdslb.com/bfs/article/f6e5c5a71e735d0affe2e1550c89e922188801893"
                                          ".jpg")

        self.a3 = get_photo_from_internet("https://i0.hdslb.com/bfs/article/a59d70a80efe44a6c5ca17e8e4d34375188801893"
                                          ".jpg")

        self.a4 = get_photo_from_internet("https://i0.hdslb.com/bfs/article/3474819e8223a34e7b525be138a74cc8188801893"
                                          ".jpg")
        self.home_b_photo = get_photo_from_internet("https://t.alcy.cc/fj/")

    def initHomeInterface(self):
        layout = MQGridLayout(self.homeInterface)
        # 创建第一个大卡片存放信息卡片
        self.home_card1 = MSimpleCardWidget()
        self.layout_home_card1 = MQGridLayout(self.home_card1)
        # self.layout_home_card1.setAlignment(Qt.AlignCenter)
        # 设置头像卡片的布局
        self.ava1 = AvatarWidget(self.a1)
        self.card1_ava_card1 = MCardWidget()
        self.layout_home_card1_ava_card1 = MQGridLayout(self.card1_ava_card1)
        self.layout_home_card1_ava_card1.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card1.addWidget(self.ava1)

        self.ava2 = AvatarWidget(self.a2)
        self.card1_ava_card2 = MCardWidget()
        self.layout_home_card1_ava_card2 = MQGridLayout(self.card1_ava_card2)
        self.layout_home_card1_ava_card2.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card2.addWidget(self.ava2)

        self.ava3 = AvatarWidget(self.a3)
        self.card1_ava_card3 = MCardWidget()
        self.layout_home_card1_ava_card3 = MQGridLayout(self.card1_ava_card3)
        self.layout_home_card1_ava_card3.setAlignment(Qt.AlignCenter)
        self.layout_home_card1_ava_card3.addWidget(self.ava3)

        self.ava4 = AvatarWidget(self.a4)
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
        self.home_card2 = MSimpleCardWidget()
        self.layout_home_card2 = MQGridLayout(self.home_card2)
        self.home_card2.clicked.connect(lambda: self.show_info_bar(self.width(), self.height()))

        # 获取天气
        if self.all_weather == [["获取失败"]]:
            self.weather_state = False
        else:
            self.weather_state = True
        self.weather_data = {}

        f = open(self.city_code, 'rb')

        # 加载JSON文件内容到Python对象
        # 使用json模块的load方法加载json数据，返回一个字典
        cities = json.load(f)
        stands = cities.keys()
        self.home_weather_card_combobox = MSearchLineEdit()
        completer = QCompleter(stands, self.home_weather_card_combobox)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        self.home_weather_card_combobox.setCompleter(completer)
        self.home_weather_card_combobox.textChanged.connect(self.weather_position_get)
        self.home_weather_re_get_button = MPushButton("重新获取")
        self.home_weather_re_get_button.clicked.connect(self.re_get_weather_button)
        # 添加城市选择到第二个大卡片
        self.layout_home_card2.addWidget(self.home_weather_card_combobox, 0, 0, 1, 2)
        self.layout_home_card2.addWidget(self.home_weather_re_get_button, 1, 0, 1, 2)

        # 添加地名到第二个大卡片
        self.card2_weather_card_label1 = MDescriptionCard((self.weather_state and "🗺️" or "⛔") + "城市名称", "未选择")
        self.layout_home_card2.addWidget(self.card2_weather_card_label1, 2, 0, 1, 1)
        # 添加天气到第二个大卡片
        self.card2_weather_card_label2 = MDescriptionCard((self.weather_state and "☁️" or "⛔") + "天气状况", "未找到")
        self.layout_home_card2.addWidget(self.card2_weather_card_label2, 2, 1, 1, 1)

        # 添加最高温到第二个大卡片
        self.card2_weather_card_label3 = MDescriptionCard((self.weather_state and "🌡️" or "⛔") + "最高气温", "未找到")
        self.layout_home_card2.addWidget(self.card2_weather_card_label3, 3, 0, 1, 1)

        # 添加最低温到第二个大卡片
        self.card2_weather_card_label4 = MDescriptionCard((self.weather_state and "🌡️" or "⛔") + "最低气温", "未找到")
        self.layout_home_card2.addWidget(self.card2_weather_card_label4, 3, 1, 1, 1)

        # 创建第三个大卡片存放图片卡片
        self.home_card3 = MSimpleCardWidget()
        self.layout_card3 = MQGridLayout(self.home_card3)

        image_label = MImageLabel()
        image_label.setImage(self.home_b_photo is None and self.resource_home_p or self.home_b_photo.scaled(1920, 1080))
        image_label.scaledToHeight(330)

        # 添加图片卡片到第三个大卡片
        self.layout_card3.addWidget(image_label)

        # 添加三个到主页面
        layout.addWidget(self.home_card3, 0, 0, 1, 2)
        layout.addWidget(self.home_card2, 0, 2, 1, 2)
        layout.addWidget(self.home_card1, 1, 0, 1, 4)

    def initAppInterface(self):
        layout = MQGridLayout(self.appInterface)
        layout.setAlignment(Qt.AlignTop)
        self.system_timer = QTimer(self.appInterface, timeout=self.run_timer)
        self.app_card1 = MSimpleCardWidget()
        self.layout_app_card1 = MFLayout(self.app_card1)
        self.layout_app_card1.setAlignment(Qt.AlignHCenter)

        # 定义倒计时
        self.timePicker = TimePicker(None, True)
        self.timePicker.setColumnFormatter(0, Utils.HoursFormatter())
        self.timePicker.setColumnFormatter(1, Utils.MinuteFormatter())
        self.timePicker.setColumnFormatter(2, Utils.SecondsFormatter())
        # 获取当前时间
        self.current_time = QTime().currentTime()

        # 定义指示器
        self.progress_circle_timer = ProgressRing()

        # 设置进度环取值范围和当前值
        self.progress_circle_timer.setRange(0, 100)

        # 显示进度环内文本
        self.progress_circle_timer.setTextVisible(True)

        # 调整进度环大小
        self.progress_circle_timer.setFixedSize(80, 80)

        # 调整厚度
        self.progress_circle_timer.setStrokeWidth(14)

        # 时间发生改变
        self.timePicker.timeChanged.connect(lambda time: self.get_calc_time(time.toString()))
        self.timer_start_button = SwitchButton()
        self.timer_start_button.setOnText("关闭倒计时")
        self.timer_start_button.setOffText("开始倒计时")
        self.timer_start_button.setFixedSize(128, 30)
        self.timer_label1 = StrongBodyLabel("倒计时时间选择->")
        self.timer_label1.setFixedSize(120, 30)
        self.timer_start_button.checkedChanged.connect(self.timer_button_action)

        self.layout_app_card1.addWidget(self.timer_label1)
        self.layout_app_card1.addWidget(self.timePicker)
        self.layout_app_card1.addWidget(self.timer_start_button)
        self.layout_app_card1.addWidget(self.progress_circle_timer)

        self.system_count_down = QTimer(self.appInterface, timeout=self.run_countdown)
        self.app_card2 = MSimpleCardWidget()
        self.layout_app_card2 = MFLayout(self.app_card2)
        self.layout_app_card2.setAlignment(Qt.AlignHCenter)
        self.countdown_start_button = SwitchButton()
        self.countdown_start_button.setOffText("开始计时")
        self.countdown_start_button.setOnText("停止计时")
        self.countdown_start_button.setFixedSize(114, 30)

        self.countdown_pause_button = MPushButton("暂停计时", ficon.PAUSE_BOLD)

        # 定义指示器
        self.progress_circle_countdown = ProgressBar()

        self.progress_circle_countdown.setRange(0, 10)

        self.progress_circle_countdown.setFormat("v")
        self.countdown_start_button.checkedChanged.connect(self.countdown_button_action)
        self.countdown_pause_button.clicked.connect(self.countdown_button_pause)
        self.countdown_label = SubtitleLabel("⌛未开始计时")
        self.layout_app_card2.addWidget(self.countdown_label)
        self.layout_app_card2.addWidget(self.countdown_start_button)

        self.layout_app_card2.addWidget(self.countdown_pause_button)
        self.layout_app_card2.addWidget(self.progress_circle_countdown)

        layout.addWidget(self.app_card1, 0, 0)
        layout.addWidget(self.app_card2, 0, 1)

    # Glayout
    # def initAppInterface(self):
    #     layout = MQGridLayout(self.appInterface)
    #     layout.setAlignment(Qt.AlignTop)
    #     self.system_timer = QTimer(self.appInterface, timeout=self.run_timer)
    #     self.app_card1 = MSimpleCardWidget()
    #     self.layout_app_card1 = MQGridLayout(self.app_card1)
    #     self.layout_app_card1.setAlignment(Qt.AlignHCenter)
    #
    #     # 定义倒计时
    #     self.timePicker = TimePicker(None, True)
    #     self.timePicker.setColumnFormatter(0, Utils.HoursFormatter())
    #     self.timePicker.setColumnFormatter(1, Utils.MinuteFormatter())
    #     self.timePicker.setColumnFormatter(2, Utils.SecondsFormatter())
    #     # 获取当前时间
    #     self.current_time = QTime().currentTime()
    #
    #     # 定义指示器
    #     self.progress_circle_timer = ProgressRing()
    #
    #     # 设置进度环取值范围和当前值
    #     self.progress_circle_timer.setRange(0, 100)
    #
    #     # 显示进度环内文本
    #     self.progress_circle_timer.setTextVisible(True)
    #
    #     # 调整进度环大小
    #     self.progress_circle_timer.setFixedSize(80, 80)
    #
    #     # 调整厚度
    #     self.progress_circle_timer.setStrokeWidth(14)
    #
    #     # 时间发生改变
    #     self.timePicker.timeChanged.connect(lambda time: self.get_calc_time(time.toString()))
    #     self.timer_start_button = SwitchButton()
    #     self.timer_start_button.setOnText("关闭倒计时")
    #     self.timer_start_button.setOffText("开始倒计时")
    #     self.timer_label1 = StrongBodyLabel("倒计时时间选择↓")
    #     self.timer_start_button.checkedChanged.connect(self.timer_button_action)
    #
    #     self.layout_app_card1.addWidget(self.timer_label1, 0, 0)
    #     self.layout_app_card1.addWidget(self.timePicker, 1, 0)
    #     self.layout_app_card1.addWidget(self.timer_start_button, 2, 0)
    #     self.layout_app_card1.addWidget(self.progress_circle_timer, 0, 1, 3, 1)
    #
    #     self.system_count_down = QTimer(self.appInterface, timeout=self.run_countdown)
    #     self.app_card2 = MSimpleCardWidget()
    #     self.layout_app_card2 = MQGridLayout(self.app_card2)
    #     self.layout_app_card2.setAlignment(Qt.AlignHCenter)
    #     self.countdown_start_button = SwitchButton()
    #     self.countdown_start_button.setOffText("开始计时")
    #     self.countdown_start_button.setOnText("停止计时")
    #
    #     self.countdown_pause_button = MPushButton("暂停计时", ficon.PAUSE_BOLD)
    #
    #     # 定义指示器
    #     self.progress_circle_countdown = ProgressBar()
    #
    #     self.progress_circle_countdown.setRange(0, 10)
    #
    #     # # 显示进度环内文本
    #     # self.progress_circle_countdown.setTextVisible(True)
    #     #
    #     # # 调整进度环大小
    #     # self.progress_circle_countdown.setFixedSize(80, 80)
    #     #
    #     # # 调整厚度
    #     # self.progress_circle_countdown.setStrokeWidth(14)
    #     self.progress_circle_countdown.setFormat("v")
    #     self.countdown_start_button.checkedChanged.connect(self.countdown_button_action)
    #     self.countdown_pause_button.clicked.connect(self.countdown_button_pause)
    #     self.countdown_label = SubtitleLabel("⌛未开始计时")
    #     self.layout_app_card2.addWidget(self.countdown_start_button, 0, 0,1,1)
    #     self.layout_app_card2.addWidget(self.countdown_label, 0, 1,2,1)
    #     self.layout_app_card2.addWidget(self.countdown_pause_button, 1, 0,1,1)
    #     self.layout_app_card2.addWidget(self.progress_circle_countdown, 2, 0,1,1)
    #
    #     layout.addWidget(self.app_card1, 0, 0)
    #     layout.addWidget(self.app_card2, 0, 1)

    def initExtendInterface(self):
        self._extend_layout = MQGridLayout(self.extendInterface)
        self._extend_layout.setAlignment(Qt.AlignTop)
        self.extend_card1 = MSimpleCardWidget()
        self.extend_card1_layout = MFLayout(self.extend_card1)
        self.extend_card1_layout.setAlignment(Qt.AlignBottom)
        self.extend_drag_edit = MLineEdit()
        self.extend_drag_edit.setFixedSize(200, 32)
        self.extend_drag_edit.setPlaceholderText("拖拽到此或者输入路径")
        self.extend_drag_edit.setClearButtonEnabled(True)
        self.extend_card1_layout.addWidget(self.extend_drag_edit)

        self.extend_start_button = MPushButton()
        self.extend_start_button.setText("开始")

        self.extend_combobox = MComboBox()
        items = ['旋转', '缩小', '模糊', '轮廓', "平滑", "锐化", "边界", "边界加强", "浮雕", "细节"]
        self.extend_combobox.addItems(items)
        self.extend_combobox.currentIndexChanged.connect(self.pixmap_get_type)
        self.extend_card1_layout.addWidget(self.extend_combobox)
        self.extend_slider = Slider(Qt.Horizontal)
        self.extend_slider_label = BodyLabel()
        self.extend_slider.setFixedWidth(180)
        self.extend_slider.setRange(0, 100)
        self.extend_slider.valueChanged.connect(self.extend_get_slider)
        self.extend_card1_layout.addWidget(self.extend_slider)
        self.extend_card1_layout.addWidget(self.extend_slider_label)
        self.extend_card1_layout.addWidget(self.extend_start_button)
        self.extend_card2 = MSimpleCardWidget()
        self.extend_card2_layout = MFLayout(self.extend_card2)
        self.extend_card2_tip = SubtitleLabel("图片预览")
        self.extend_card2_layout.addWidget(self.extend_card2_tip)
        self.pixmap = MImageLabel()
        self.cut_b = MPushButton("裁剪")
        self.cut_b.clicked.connect(self.cut_pic)

        self.extend_card2_layout.addWidget(self.cut_b)
        self.extend_drag_edit.textChanged.connect(self.file_dir_get)
        self.extend_start_button.clicked.connect(self.handle_pixmap)
        self._extend_layout.setColumnStretch(0, 2)
        self._extend_layout.setColumnStretch(1, 3)
        self._extend_layout.addWidget(self.extend_card1, 0, 0, 1, 1)
        self._extend_layout.addWidget(self.extend_card2, 0, 1, 1, 1)

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
            image=self.resource_gif1,
            isClosable=True
        )

        # add button to view

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 15)
        view.widgetLayout.addSpacing(11)

        # show view
        w = Flyout.make(view, self.card1_ava_card1, self, aniType=FlyoutAnimationType.SLIDE_RIGHT)
        view.closed.connect(w.close)

    def get_calc_time(self, time: str):
        try:
            time = time.split(":")
            self.calc_time = Utils.time_to_seconds(time)
        except Exception as e:
            self.show_info_bar(str(e))

    def timer_button_action(self):
        res = self.timer_start_button.checked
        try:
            if res:
                self.timer_start_button.setOnText("关闭倒计时")
                self.system_timer.start(1000)
                self.show_info_bar("开始", "success", "倒计时")
            else:
                self.timer_start_button.setOffText("开始倒计时")
                self.time_count = 0
                self.progress_circle_timer.setValue(0)
                self.system_timer.stop()
                self.show_info_bar("关闭", "success", "倒计时")
        except Exception as e:
            self.show_info_bar(str(e))

    def run_timer(self):
        self.time_count += 1
        try:
            percent = int((self.time_count / self.calc_time) * 100)
            if percent > 100:
                self.timer_start_button.setChecked(False)
                self.show_info_bar("倒计时完成", "success", "计时器")
            else:
                self.progress_circle_timer.setValue(percent)
        except Exception as e:
            self.show_info_bar(str(e))

    def countdown_button_action(self):
        res = self.countdown_start_button.checked
        try:
            if res:
                self.system_count_down.start(100)
                self.show_info_bar("开始", "success", "计时")
                # self.progress_circle_countdown.start()
            else:
                self.countdown_pause_button.setText("暂停计时")
                self.countdown_pause_button.setIcon(ficon.PAUSE_BOLD)
                self.system_count_down.stop()
                self.show_info_bar("关闭", "success", "计时")
                self.countdown_label.setText("⌛未开始计时")
                # self.progress_circle_countdown.stop()
                self.countdown_count = 0
                self.progress_circle_countdown.setValue(self.countdown_count)
        except Exception as e:
            self.show_info_bar(str(e))

    def countdown_button_pause(self):
        try:
            if self.countdown_start_button.checked:

                if self.countdown_pause_flag:
                    self.countdown_pause_button.setText("暂停计时")
                    self.countdown_pause_button.setIcon(ficon.PAUSE_BOLD)
                    self.system_count_down.start(100)
                    self.show_info_bar("恢复", "success", "计时")
                else:
                    self.countdown_pause_button.setText("恢复计时")
                    self.countdown_pause_button.setIcon(ficon.PLAY_SOLID)
                    self.system_count_down.stop()
                    self.show_info_bar("暂停", "success", "计时")
                self.countdown_pause_flag = not self.countdown_pause_flag
        except Exception as e:
            self.show_info_bar(str(e))

    def run_countdown(self):
        self.countdown_count += 1
        s = int(self.countdown_count / 10)
        self.progress_circle_countdown.setValue(self.countdown_count % 10 + 1)
        res = Utils.second_to_time(s)
        self.countdown_label.setText(f"  {res[0]}小时-{res[1]}分-{res[2]}秒")

    def file_dir_get(self):
        res = self.extend_drag_edit.text()

        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.file_dir = self.extend_drag_edit.text()
        if len(res.split("/")) >= 2:
            try:
                self.extend_card2_layout.removeWidget(self.pixmap)
                self.pix = QPixmap(self.file_dir)
                pixh = self.pix.height()
                pixw = self.pix.width()
                l = pixh / self.pic_h
                self.pic_w = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
                self.extend_card2_layout.addWidget(self.pixmap)
                self.extend_card2.setFixedSize(int(self.pic_w) + 40, 380)
            except Exception as e:
                self.show_info_bar(str(e))

    def cut_pic(self):
        if self.file_dir == "":
            self.show_info_bar("路径为空", "error", "错误")
        else:
            try:
                to = self.file_dir.split("/")
                pit_name = to[-1]
                im = Image.open(self.file_dir)
                print(self.pix.height()/self.pic_h)
                new_size = (self.pixmap.get_qrect()[0] * (self.pix.width()/self.pic_w), self.pixmap.get_qrect()[1] * (self.pix.width()/self.pic_w), self.pixmap.get_qrect()[2] * (self.pix.height()/self.pic_h), self.pixmap.get_qrect()[3] * (self.pix.height()/self.pic_h))
                print(self.pixmap.get_qrect(), new_size)

                handled = im.crop(new_size)
                fix_name = f"crop()+{pit_name}"
                new_file = self.current_dir + "/" + fix_name
                handled.save(new_file)
                self.extend_card2_layout.removeWidget(self.pixmap)
                self.pix = QPixmap(new_file)
                pixh = self.pix.height()
                pixw = self.pix.width()
                l = pixh / self.pic_h
                self.pic_w = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
                self.extend_card2_layout.addWidget(self.pixmap)
                self.extend_card2.setFixedSize(int(self.pic_w) + 40, 380)
                self.extend_drag_edit.setText(new_file)
                self.file_dir_get()
            except Exception as e:
                self.show_info_bar(str(e))

    def handle_pixmap(self):
        Utils.create_file_dir()
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
                l = pixh / self.pic_h
                self.pic_w = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
                self.extend_card2_layout.addWidget(self.pixmap)
                self.extend_card2.setFixedSize(int(self.pic_w) + 40, 380)
                self.extend_drag_edit.setText(new_file)
                self.file_dir_get()
            except Exception as e:
                self.show_info_bar(str(e))

    def pixmap_get_type(self):
        res = self.extend_combobox.currentText()
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        if res != "旋转" and res != "缩小" and res != "模糊":
            self.extend_slider.hide()
            self.extend_slider_label.hide()
        else:
            self.extend_slider.show()
            self.extend_slider_label.show()
        self.pixmap_type = res

    def weather_position_get(self):
        res = self.home_weather_card_combobox.text()
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.weather_position = res
        if len(self.weather_position) == 0:
            return
        if '\u4e00' <= self.weather_position[0] <= '\u9fff':
            try:
                data = re_get_weather(self.weather_position, self.city_code)
                self.card2_weather_card_label1.setDes(data[0])
                self.card2_weather_card_label2.setDes(data[1])
                self.card2_weather_card_label3.setDes(data[2])
                self.card2_weather_card_label4.setDes(data[3])
            except Exception as e:
                self.card2_weather_card_label1.setDes("未选择")
                self.card2_weather_card_label2.setDes("未找到")
                self.card2_weather_card_label3.setDes("未找到")
                self.card2_weather_card_label4.setDes("未找到")

    def re_get_weather_button(self):
        if len(self.weather_position) == 0:
            return
        if '\u4e00' <= self.weather_position[0] <= '\u9fff':
            try:
                data = re_get_weather(self.weather_position, self.city_code)
                self.card2_weather_card_label1.setDes(data[0])
                self.card2_weather_card_label2.setDes(data[1])
                self.card2_weather_card_label3.setDes(data[2])
                self.card2_weather_card_label4.setDes(data[3])
                self.show_info_bar("获取成功", "success", self.weather_position)
            except Exception as e:
                self.card2_weather_card_label1.setDes("未选择")
                self.card2_weather_card_label2.setDes("未找到")
                self.card2_weather_card_label3.setDes("未找到")
                self.card2_weather_card_label4.setDes("未找到")
                self.show_info_bar("获取失败", "error", self.weather_position)

    def extend_get_slider(self):
        res = self.extend_slider.value() / 100
        self.extend_slider_label.setText(str(self.extend_slider.value()) + "%")
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.extend_slider_value = res

    def tickcount_upd(self):
        self.frametime += 1


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    QtWidgets.qApp.processEvents()  # 处理主进程事件
    w = Window()
    w.show()
    app.exec_()
