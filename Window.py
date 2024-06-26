# coding:utf-8
import os
import sys
from datetime import datetime

from PIL import Image, ImageFilter
from PyQt5 import sip
from PyQt5.QtCore import QTime, QTimer, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QCompleter, QWidget, QApplication, QListWidgetItem
from qfluentwidgets import FlyoutView, Flyout, FlyoutAnimationType, \
    TimePicker, ProgressRing, Slider, SwitchButton, ProgressBar, StrongBodyLabel, \
    SubtitleLabel, SplashScreen, toggleTheme, FluentIcon, VBoxLayout, SwitchSettingCard, \
    HyperlinkCard, ColorDialog, PushSettingCard, ListWidget
from qfluentwidgets import (NavigationItemPosition, MSFluentWindow, AvatarWidget, InfoBar, InfoBarPosition,
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


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
            sip.delete(child)


class Window(MSFluentWindow):
    THEME_COLOR = "#b9beed"
    RESOURCE_AVA = "resource/ava.png"
    RESOURCE_LOGO = "resource/logo.png"
    RESOURCE_CITY = "resource/city_to_code.json"
    RESOURCE_HOME = "resource/home.png"
    RESOURCE_GIF1 = "resource/1.gif"
    RESOURCE_GIF2 = "resource/2.gif"
    TODO_FILE = "todo.json"

    def __init__(self):
        super().__init__()
        self.todo_selected_index = 9999
        self.todo_data_text = ""
        self.cut_b = None
        self.todo_title_text = ""
        self.setting_layout = None
        self.home_layout = None
        self.splashScreen = None
        self.home_b_photo = None
        self.splash = None
        self.desktop = QApplication.desktop().availableGeometry()
        self.pc_w, self.pc_h = self.desktop.width(), self.desktop.height()
        self.progress_circle_timer = None
        self.timer_pause_button = None
        self.timer_label = SubtitleLabel()
        self.timer_start_button = SwitchButton()
        self.timer_pause_flag = False
        self.system_count_down = QTimer()
        self._extend_layout = MQGridLayout(None)
        self.home_weather_re_get_button = MPushButton()
        self.extend_slider_label = BodyLabel()
        setTheme(Theme.DARK)
        setThemeColor(self.THEME_COLOR)

        self.pic_h = 400
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
        self.resource_ava = Utils.get_path(self.RESOURCE_AVA)
        self.city_code = Utils.get_path(self.RESOURCE_CITY)
        self.resource_logo = Utils.get_path(self.RESOURCE_LOGO)
        self.resource_home_p = Utils.get_path(self.RESOURCE_HOME)
        self.resource_gif1 = Utils.get_path(self.RESOURCE_GIF1)
        self.resource_gif2 = Utils.get_path(self.RESOURCE_GIF2)
        self.a1 = QPixmap(self.resource_ava)
        self.a2 = QPixmap(self.resource_ava)
        self.a3 = QPixmap(self.resource_ava)
        self.a4 = QPixmap(self.resource_ava)
        self.calc_time = 300
        self.system_countdown = None
        self.layout_app_card1 = None
        self.timePicker = None
        self.countdown_start_button = SwitchButton()
        self.countdown_label1 = None
        self.countdown_label2 = None
        self.current_time = None
        self.app_card1 = None
        self.progress_circle_countdown = None
        self.time_count = 0
        self.timer_count = 0
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
        self.root_dir = os.getcwd().replace("\\", "/")
        Utils.create_json_file(self.root_dir)

        self.current_dir = self.root_dir + "/Texture/"
        self.extend_slider_value = 0
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
        self.settingInterface = Widget('setting', self)
        self.initWindow()
        self.get_internet_data()
        self.initHomeInterface()
        self.initAppInterface()
        self.initExtendInterface()
        self.initSettings()
        self.initNavigation()
        self.ref_todo_list()
        self.splashScreen.finish()
        self.start_animation_pos = MAnimation(self, b'pos', QPoint(self.pc_w // 2 - self.width() // 2, self.pc_h + 46),
                                              QPoint(self.pc_w // 2 - self.width() // 2,
                                                     self.pc_h // 2 - self.height() // 2),
                                              1100)
        self.start_animation_pos.start()
        self.start_animation_alpha = MAnimation(self, b'windowOpacity', 0, 1, 1100)
        self.start_animation_alpha.start()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, ficon.HOME, '主页', ficon.HOME_FILL, NavigationItemPosition.TOP,
                             False)
        self.addSubInterface(self.appInterface, ficon.DATE_TIME, '时钟', ficon.DATE_TIME, NavigationItemPosition.TOP,
                             False)
        self.addSubInterface(self.extendInterface, ficon.PHOTO, '图片处理', ficon.PHOTO, NavigationItemPosition.TOP,
                             False)
        self.addSubInterface(self.settingInterface, ficon.SETTING, "设置", ficon.SETTING, NavigationItemPosition.BOTTOM,
                             False)

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(936, 674)
        self.setWindowIcon(QIcon(self.resource_logo))
        self.setWindowTitle('多任务助手')
        self.desktop = QApplication.desktop().availableGeometry()
        self.move(self.pc_w // 2 - self.width() // 2, self.pc_h // 2 - self.height() // 2)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(402, 402))
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
        self.home_layout = MQGridLayout(self.homeInterface)
        # 创建第一个大卡片存放信息卡片
        self.home_layout.setColumnStretch(0, 3)
        self.home_layout.setColumnStretch(1, 1)
        self.home_layout.setRowStretch(0, 2)
        self.home_layout.setRowStretch(1, 1)
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

        self.card1_ava_card1.clicked.connect(
            lambda: self.show_flyout_view(self.card1_ava_card1, "毕天宇", "202209160316", self.resource_gif2))
        self.card1_ava_card2.clicked.connect(
            lambda: self.show_flyout_view(self.card1_ava_card2, "赵锐", "202209160307", self.resource_gif1))
        self.card1_ava_card3.clicked.connect(
            lambda: self.show_flyout_view(self.card1_ava_card3, "陈影茜", "202209160305", self.resource_gif1))
        self.card1_ava_card4.clicked.connect(
            lambda: self.show_flyout_view(self.card1_ava_card4, "魏艳", "202209160301", self.resource_gif1))
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
        cities = json.load(f)
        stands = cities.keys()
        self.home_weather_card_combobox = MSearchLineEdit()
        completer = QCompleter(stands, self.home_weather_card_combobox)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        self.home_weather_card_combobox.setCompleter(completer)
        self.home_weather_card_combobox.textChanged.connect(self.weather_position_get)
        self.home_weather_re_get_button = MPushButton("重新获取", ficon.CLOUD)
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

        image_label = MImageLabel(candraw=False)
        image_label.setImage(self.home_b_photo is None and self.resource_home_p or self.home_b_photo)
        image_label.scaledToHeight(630)
        sl = MSmoothScrollArea(image_label)
        # 添加图片卡片到第三个大卡片
        self.layout_card3.addWidget(sl)
        # 添加三个到主页面
        self.home_layout.addWidget(self.home_card3, 0, 0, 1, 1)
        self.home_layout.addWidget(self.home_card2, 0, 1, 1, 1)
        self.home_layout.addWidget(self.home_card1, 1, 0, 1, 2)

    def initAppInterface(self):
        self.app_layout = MQGridLayout(self.appInterface)
        self.app_layout.setAlignment(Qt.AlignTop)
        self.system_countdown = QTimer(self.appInterface, timeout=self.run_countdown)
        self.app_card1 = MSimpleCardWidget()
        self.layout_app_card1 = MFLayout(self.app_card1)

        # 定义倒计时
        self.timePicker = TimePicker(None, True)
        self.timePicker.setColumnFormatter(0, Utils.HoursFormatter())
        self.timePicker.setColumnFormatter(1, Utils.MinuteFormatter())
        self.timePicker.setColumnFormatter(2, Utils.SecondsFormatter())
        # 获取当前时间
        self.current_time = QTime().currentTime()

        # 定义指示器
        self.progress_circle_countdown = ProgressRing()

        # 设置进度环取值范围和当前值
        self.progress_circle_countdown.setRange(0, 100)

        # 显示进度环内文本
        self.progress_circle_countdown.setTextVisible(True)

        # 调整进度环大小
        self.progress_circle_countdown.setFixedSize(80, 80)

        # 调整厚度
        self.progress_circle_countdown.setStrokeWidth(14)

        # 时间发生改变
        self.timePicker.timeChanged.connect(lambda time: self.get_calc_time(time.toString()))
        self.countdown_start_button = SwitchButton()
        self.countdown_start_button.setOnText("关闭倒计时")
        self.countdown_start_button.setOffText("开始倒计时")
        self.countdown_start_button.setFixedSize(128, 30)
        self.countdown_label1 = StrongBodyLabel("倒计时时间选择->")
        self.countdown_label1.setFixedSize(120, 30)
        self.countdown_start_button.checkedChanged.connect(self.countdown_button_action)

        self.layout_app_card1.addWidget(self.countdown_label1)
        self.layout_app_card1.addWidget(self.timePicker)
        self.layout_app_card1.addWidget(self.countdown_start_button)
        self.layout_app_card1.addWidget(self.progress_circle_countdown)

        self.system_count_down = QTimer(self.appInterface, timeout=self.run_timer)
        self.app_card2 = MSimpleCardWidget()
        self.layout_app_card2 = MFLayout(self.app_card2)
        self.timer_start_button = SwitchButton()
        self.timer_start_button.setOffText("开始计时")
        self.timer_start_button.setOnText("停止计时")
        self.timer_start_button.setFixedSize(114, 30)

        self.timer_pause_button = MPushButton("暂停计时", ficon.PAUSE_BOLD)

        # 定义指示器
        self.progress_circle_timer = ProgressBar()

        self.progress_circle_timer.setRange(0, 10)

        self.progress_circle_timer.setFormat("v")
        self.timer_start_button.checkedChanged.connect(self.timer_button_action)
        self.timer_pause_button.clicked.connect(self.timer_button_pause)
        self.timer_label = SubtitleLabel("⌛未开始计时")
        self.layout_app_card2.addWidget(self.timer_label)
        self.layout_app_card2.addWidget(self.timer_start_button)
        self.layout_app_card2.addWidget(self.timer_pause_button)
        self.layout_app_card2.addWidget(self.progress_circle_timer)

        self.app_card3 = MSimpleCardWidget()
        self.layout_app_card3 = MQGridLayout(self.app_card3)
        self.layout_app_card3.setAlignment(Qt.AlignTop)
        self.todo_data = MLineEdit()
        self.todo_data.setPlaceholderText("输入待办")
        self.todo_data.textChanged.connect(self.todo_get_data)
        self.layout_app_card3.addWidget(self.todo_data)

        self.todo_add_button = MPushButton("添加待办", ficon.FOLDER_ADD)
        self.todo_add_button.clicked.connect(self.todo_add_data)
        self.layout_app_card3.addWidget(self.todo_add_button)

        self.todo_delete_button = MPushButton("删除待办", ficon.DELETE)
        self.todo_delete_button.clicked.connect(self.todo_delete_data)
        self.layout_app_card3.addWidget(self.todo_delete_button)

        self.app_card4 = MSimpleCardWidget()
        self.layout_app_card4 = MQGridLayout(self.app_card4)
        self.layout_app_card4.setAlignment(Qt.AlignTop)
        self.todo_list = ListWidget()
        self.todo_list.itemClicked.connect(self.todo_list_click)
        self.layout_app_card4.addWidget(self.todo_list)
        self.app_layout.addWidget(self.app_card1, 0, 0)
        self.app_layout.addWidget(self.app_card2, 0, 1)
        self.app_layout.addWidget(self.app_card3, 1, 0)
        self.app_layout.addWidget(self.app_card4, 1, 1)

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

        self.extend_start_button = MPushButton("开始", ficon.PLAY_SOLID)

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
        self.cut_b = MPushButton("裁剪", ficon.CUT)
        self.cut_b.clicked.connect(self.cut_pic)

        self.extend_card2_layout.addWidget(self.cut_b)
        self.extend_drag_edit.textChanged.connect(self.file_dir_get)
        self.extend_start_button.clicked.connect(self.handle_pixmap)
        self._extend_layout.setColumnStretch(0, 2)
        self._extend_layout.setColumnStretch(1, 3)
        self._extend_layout.addWidget(self.extend_card1, 0, 0, 1, 1)
        self._extend_layout.addWidget(self.extend_card2, 0, 1, 1, 1)

    def initSettings(self):
        self.setting_layout = VBoxLayout(self.settingInterface)
        self.setting_layout.setContentsMargins(20, 20, 20, 20)
        self.setting_layout.setAlignment(Qt.AlignTop)
        card = SwitchSettingCard(
            icon=FluentIcon.BRIGHTNESS,
            title="亮暗主题切换",
            content="亮暗主题切换",
            ontext="暗色",
            offtext="亮色"
        )
        card.checkedChanged.connect(lambda: toggleTheme(False))

        cardmica = SwitchSettingCard(
            icon=FluentIcon.TRANSPARENT,
            title="是否开启Mica效果",
            content="打开Mica提高画面的质感，但是会增加能耗",
            ontext="打开",
            offtext="关闭"
        )
        cardmica.setValue(True)
        cardmica.checkedChanged.connect(lambda x: self.setMicaEffectEnabled(x))

        cardtheme = PushSettingCard(
            text="选择颜色",
            icon=FluentIcon.PALETTE,
            title="主题颜色",
            content="更改主题颜色"
        )
        cardtheme.clicked.connect(self.show_color_picker)

        cardlink = HyperlinkCard(
            url="https://gitee.com/baishang1337/mypython_-project",
            text="打开Gitee项目链接",
            icon=FluentIcon.LINK,
            title="打开Gitee项目链接",
            content="获得更多项目信息"
        )

        self.setting_layout.addWidget(card)
        self.setting_layout.addWidget(cardmica)
        self.setting_layout.addWidget(cardtheme)
        self.setting_layout.addWidget(cardlink)

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

    def todo_list_click(self):
        self.todo_selected_index = self.todo_list.currentRow()
        ys = {
            0: False,
            2: True
        }

        try:
            data = Utils.read_file(self.TODO_FILE, self.root_dir)
            state = self.todo_list.item(self.todo_selected_index).checkState()
            data[self.todo_selected_index]["state"] = ys[state]
            Utils.create_file(self.TODO_FILE, self.root_dir, data)
        except Exception as e:
            self.show_info_bar(content="未选择项", typ="warning")

    def todo_get_data(self):
        self.todo_data_text = self.todo_data.text()

    def todo_delete_data(self):
        Utils.create_json_file(self.TODO_FILE, self.root_dir)
        if self.todo_selected_index == 9999:
            self.show_info_bar(content="未选择删除项", typ="warning")
        else:
            data = Utils.read_file(self.TODO_FILE, self.root_dir)
            for i, e in enumerate(data):
                if i == self.todo_selected_index:
                    data.pop(i)
                    Utils.create_file(self.TODO_FILE, self.root_dir, data)
            self.show_info_bar(content="删除成功", typ="success")
            self.ref_todo_list()

    def todo_add_data(self):
        Utils.create_json_file(self.TODO_FILE, self.root_dir)
        if self.todo_data_text == "":
            self.show_info_bar(content="请输入待办事项", typ="warning")
        else:
            try:
                data = Utils.read_file(self.TODO_FILE, self.root_dir)
                data.append({"data": self.todo_data_text, "state": False, "time": str(datetime.now().strftime("%Y-%m"
                                                                                                              "-%d "
                                                                                                              "%H:%M:%S"
                                                                                                              ))})
                Utils.create_file(self.TODO_FILE, self.root_dir, data)
                self.show_info_bar(content="添加成功", typ="success")
                self.ref_todo_list()
            except Exception as e:
                print(e)

    def ref_todo_list(self):
        Utils.create_json_file(self.TODO_FILE, self.root_dir)
        ys = {
            False: Qt.Unchecked,
            True: Qt.Checked
        }
        self.todo_list.clear()
        data = Utils.read_file(self.TODO_FILE, self.root_dir)
        for i, e in enumerate(data):
            item = QListWidgetItem(f"{e["data"]} ({e["time"]})")
            item.setCheckState(ys[e["state"]])
            self.todo_list.addItem(item)

    def show_color_picker(self):
        w = ColorDialog(QColor(self.THEME_COLOR), "选择主题颜色", self.settingInterface, enableAlpha=False)
        w.colorChanged.connect(lambda color: self.set_theme_color(color))
        w.exec()

    def set_theme_color(self, a):
        self.THEME_COLOR = a.name()
        setThemeColor(self.THEME_COLOR)

    def show_flyout_view(self, to, title="", content="", img=""):
        """
        显示弹出视图。

        创建一个弹出视图，配置标题、内容、图像和可关闭性。然后，通过添加间距来调整视图内部组件的布局。
        最后，使用飞出动画方式显示视图，并在视图关闭时关联关闭操作。
        """
        # 创建弹出视图，配置标题、内容、图像和是否可关闭
        view = FlyoutView(
            title=title,
            content=content,
            image=img,
            isClosable=True
        )

        # 调整视图内部布局的间距，以优化显示效果
        view.widgetLayout.insertSpacing(1, 15)
        view.widgetLayout.addSpacing(11)

        # 使用飞出动画方式显示视图，并在视图关闭时关联关闭操作
        w = Flyout.make(view, to, self, aniType=FlyoutAnimationType.SLIDE_RIGHT)
        view.closed.connect(w.close)

    def get_calc_time(self, time: str):
        """
        将输入的时间字符串转换为总秒数。

        尝试将时间字符串按照冒号分隔，然后通过Utils类的静态方法time_to_seconds转换为秒。
        如果转换过程中发生异常，则通过show_info_bar方法显示异常信息。

        参数:
        time (str): 表示时间的字符串，格式为"hh:mm"。

        异常:
        可能抛出任何在时间转换过程中发生的异常。
        """
        try:
            # 将时间字符串按冒号分割成小时和分钟
            time = time.split(":")
            # 将分割后的时间转换为总秒数
            self.calc_time = Utils.time_to_seconds(time)
        except Exception as e:
            # 显示异常信息
            self.show_info_bar(str(e))

    def countdown_button_action(self):
        """
        处理倒计时启动按钮的点击事件。

        根据按钮的当前状态（选中或未选中），启动或停止倒计时，并相应地更新用户界面元素。
        """
        # 检查倒计时启动按钮的选中状态
        res = self.countdown_start_button.checked
        try:
            if res:
                # 当按钮被选中时，启动倒计时，并更新按钮文本
                self.countdown_start_button.setOnText("关闭倒计时")
                self.system_countdown.start(1000)  # 以1秒为间隔启动倒计时
                self.show_info_bar("开始", "success", "倒计时")  # 显示开始倒计时的信息
            else:
                # 当按钮未被选中时，停止倒计时，并重置相关界面元素
                self.countdown_start_button.setOffText("开始倒计时")
                self.time_count = 0  # 重置时间计数器
                self.progress_circle_countdown.setValue(0)  # 重置进度圈的值
                self.system_countdown.stop()  # 停止倒计时
                self.show_info_bar("关闭", "success", "倒计时")  # 显示关闭倒计时的信息
        except Exception as e:
            # 在发生异常时，通过信息栏显示异常信息
            self.show_info_bar(str(e))

    def run_countdown(self):
        """
        执行倒计时逻辑。

        每次调用此方法时，都会增加时间计数器，并根据计算出的百分比更新倒计时进度。
        如果倒计时完成，将关闭倒计时启动按钮并显示成功消息。
        如果在计算过程中发生异常，将显示异常信息。
        """

        # 增加时间计数器
        self.time_count += 1

        try:
            # 计算当前倒计时的百分比
            percent = int((self.time_count / self.calc_time) * 100)

            # 如果倒计时已完成
            if percent > 100:
                # 关闭倒计时启动按钮，并显示倒计时完成的消息
                self.countdown_start_button.setChecked(False)
                self.show_info_bar("倒计时完成", "success", "计时器")
            else:
                # 更新倒计时进度圈的值
                self.progress_circle_countdown.setValue(percent)
        except Exception as e:
            # 如果发生异常，显示异常信息
            self.show_info_bar(str(e))

    def timer_button_action(self):
        """
        处理计时器按钮的动作。

        根据计时器启动按钮的选中状态，开始或停止计时器。如果计时器已经开始，则暂停计时器；
        如果计时器未开始，则启动计时器。
        """
        # 检查计时器启动按钮的选中状态
        res = self.timer_start_button.checked

        try:
            if res:
                # 如果按钮被选中，开始计时
                self.system_count_down.start(100)
                # 显示开始计时的信息栏
                self.show_info_bar("开始", "success", "计时")
            else:
                # 如果按钮未被选中，暂停/停止计时
                self.timer_pause_button.setText("暂停计时")
                self.timer_pause_button.setIcon(ficon.PAUSE_BOLD)
                self.system_count_down.stop()
                # 显示停止计时的信息栏
                self.show_info_bar("关闭", "success", "计时")
                # 重置计时标签文本和计时值
                self.timer_label.setText("⌛未开始计时")
                self.timer_count = 0
                self.progress_circle_timer.setValue(self.timer_count)
        except Exception as e:
            # 如果发生异常，显示异常信息
            self.show_info_bar(str(e))

    def timer_button_pause(self):
        """
        控制计时器的暂停和恢复功能。

        当计时器开始运行后，此函数用于切换计时器的暂停状态。
        如果计时器处于暂停状态，它将恢复计时；
        如果计时器处于运行状态，它将暂停计时。
        """
        try:
            # 检查计时器启动按钮是否被选中
            if self.timer_start_button.checked:
                # 切换计时器的暂停状态
                if self.timer_pause_flag:
                    # 如果当前处于暂停状态，更新按钮为恢复计时，并启动计时器
                    self.timer_pause_button.setText("暂停计时")
                    self.timer_pause_button.setIcon(ficon.PAUSE_BOLD)
                    self.system_count_down.start(100)
                    self.show_info_bar("恢复", "success", "计时")
                else:
                    # 如果当前不处于暂停状态，更新按钮为暂停计时，并停止计时器
                    self.timer_pause_button.setText("恢复计时")
                    self.timer_pause_button.setIcon(ficon.PLAY_SOLID)
                    self.system_count_down.stop()
                    self.show_info_bar("暂停", "success", "计时")
                # 切换计时器的暂停标志
                self.timer_pause_flag = not self.timer_pause_flag
        except Exception as e:
            # 如果发生异常，通过信息栏显示异常信息
            self.show_info_bar(str(e))

    def run_timer(self):
        """
        运行定时器函数，每秒执行一次来更新计时器的显示。

        此函数主要负责更新计时器的进度圈和文字标签，显示倒计时的剩余时间。
        """
        # 自增计时器计数，用于计算已经过去的时间
        self.timer_count += 1
        # 计算已经过去的时间（秒），用于后续转换为小时、分钟和秒的格式
        s = int(self.timer_count / 10)
        # 更新进度圈的值，显示当前计时器的进度
        self.progress_circle_timer.setValue(self.timer_count % 10 + 1)
        # 将秒数转换为小时、分钟和秒的格式，用于更新计时器的文字标签
        res = Utils.second_to_time(s)
        # 更新计时器标签的文本，显示倒计时的剩余时间
        self.timer_label.setText(f"  {res[0]}小时-{res[1]}分-{res[2]}秒")

    def file_dir_get(self):
        """
        获取扩展拖拽编辑框中的文本内容，并根据该内容处理图片显示。

        如果文本表示的路径包含至少两个目录层级，则尝试加载该路径下的图片，并根据图片的尺寸调整显示大小。
        如果加载图片过程中发生异常，将异常信息显示在信息栏中。
        """
        # 获取扩展拖拽编辑框中的文本
        res = self.extend_drag_edit.text()

        # 保存文件目录路径
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.file_dir = self.extend_drag_edit.text()

        # 检查路径是否包含至少两个目录，以确保它是有效的图片路径
        if len(res.split("/")) >= 2:
            try:
                # 如果已经存在pixmaps，先从布局中移除
                self.extend_card2_layout.removeWidget(self.pixmap)
                # 加载新的图片
                self.pix = QPixmap(self.file_dir)
                # 获取图片的高度和宽度
                pixh = self.pix.height()
                pixw = self.pix.width()
                # 计算比例，用于等比例调整图片大小
                l = pixh / self.pic_h
                self.pic_w = pixw // l
                # 调整图片大小并设置到pixmap上
                self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
                # 将处理后的图片添加到布局中
                self.extend_card2_layout.addWidget(self.pixmap)
            except Exception as e:
                # 如果在处理图片过程中发生异常，显示异常信息
                self.show_info_bar(str(e))

    def cut_pic(self):
        """
        根据当前设置的文件目录和图片参数，裁剪图片并显示裁剪后的图片。
        如果文件目录为空，则显示错误信息。
        裁剪比例基于原始图片宽度和高度与目标宽度和高度的比例。
        """
        # 检查文件目录是否为空，如果为空，则显示错误信息
        if self.file_dir == "":
            self.show_info_bar("路径为空", "error", "错误")
        else:
            try:
                # 分割文件路径获取图片名称
                to = self.file_dir.split("/")
                pit_name = to[-1]
                # 打开图片文件
                with Image.open(self.file_dir) as im:
                    # 计算裁剪比例并打印验证
                    # 根据裁剪比例计算新图片的尺寸
                    new_size = (self.pixmap.get_qrect()[0] * (self.pix.width() / self.pic_w),
                                self.pixmap.get_qrect()[1] * (self.pix.width() / self.pic_w),
                                self.pixmap.get_qrect()[2] * (self.pix.height() / self.pic_h),
                                self.pixmap.get_qrect()[3] * (self.pix.height() / self.pic_h))

                    # 对图片进行裁剪
                    handled = im.crop(new_size)
                # 生成新的文件名
                fix_name = f"crop()+{pit_name}"
                # 拼接新的文件路径并保存裁剪后的图片
                new_file = self.current_dir + "/" + fix_name
                handled.save(new_file)

                # 从布局中移除旧的图片组件，加载新的裁剪后的图片
                self.extend_card2_layout.removeWidget(self.pixmap)
                self.pix = QPixmap(new_file)
                pixh = self.pix.height()
                pixw = self.pix.width()
                l = pixh / self.pic_h
                self.pic_w = pixw // l
                self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
                self.extend_card2_layout.addWidget(self.pixmap)

                # 更新文件路径显示
                self.extend_drag_edit.setText(new_file)
                # 更新文件目录
                self.file_dir_get()
            except Exception as e:
                # 如果在处理过程中发生异常，则显示异常信息
                self.show_info_bar(str(e))

    def handle_pixmap(self):
        """
        处理图片文件，根据用户选择的图片处理类型（如旋转、缩小、模糊等），对图片进行相应处理。
        创建新的图片文件，并在界面中显示处理后的图片。
        """
        try:
            # 创建文件夹
            Utils.create_file_dir()
            # 检查文件目录是否为空
            if not self.file_dir:
                self.show_info_bar("路径为空", "error", "错误")
                return

            # 分割文件路径获取文件名
            to = self.file_dir.split('/')
            pit_name = to[-1]
            # 打开图片文件
            with Image.open(self.file_dir) as im:
                # 获取滑块的值，用于确定图片处理的程度
                slider_value = self.extend_slider_value

                # 根据图片处理类型进行不同的操作
                handled, fix_name = self.process_image(im, slider_value, pit_name)
                new_file = os.path.join(self.current_dir, fix_name)

            # 保存处理后的图片
            handled.save(new_file)
            # 更新UI显示处理后的图片
            self.update_ui(new_file)

        except Exception as e:
            # 显示处理异常信息
            self.show_info_bar(str(e))

    def process_image(self, image, slider_value, pit_name):
        """
        根据不同的处理类型对图片进行处理。
        """
        handled = None
        fix_name = ""
        match self.pixmap_type:
            case "旋转":
                handled = image.rotate(int(slider_value * 360))
                fix_name = f"rotate({str(int(slider_value * 360))}){pit_name}"
            case "缩小":
                # 计算缩小比例
                q = slider_value == 0 and 0.1 or slider_value
                # 计算新的尺寸
                tup = (int(image.size[0] * q), int(image.size[1] * q))
                handled = image.resize(tup)
                fix_name = f"resize({str(tup)}){pit_name}"

            case "模糊":
                # 模糊图片
                handled = image.filter(ImageFilter.GaussianBlur(int(slider_value * 100)))
                fix_name = f"blur({int(slider_value * 100)}){pit_name}"
            case "轮廓":
                # 提取图片轮廓
                handled = image.filter(ImageFilter.CONTOUR)
                fix_name = f"(contour){pit_name}"
            case "平滑":
                # 平滑图片
                handled = image.filter(ImageFilter.SMOOTH_MORE)
                fix_name = f"(smooth){pit_name}"
            case "锐化":
                # 锐化图片
                handled = image.filter(ImageFilter.SHARPEN)
                fix_name = f"(sharpen){pit_name}"
            case "边界":
                # 提取图片边界
                handled = image.filter(ImageFilter.FIND_EDGES)
                fix_name = f"(find_edges){pit_name}"
            case "边界加强":
                # 加强图片边界
                handled = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                fix_name = f"(edge_enhance){pit_name}"
            case "浮雕":
                # 浮雕效果处理图片
                handled = image.filter(ImageFilter.EMBOSS)
                fix_name = f"(emboss){pit_name}"
            case "细节":
                # 强化图片细节
                handled = image.filter(ImageFilter.DETAIL)
                fix_name = f"(detail){pit_name}"
            # 其他处理类型...
        return handled, fix_name

    def update_ui(self, new_file):
        """
        更新UI以显示处理后的图片。
        """
        # 从布局中移除原始图片
        self.extend_card2_layout.removeWidget(self.pixmap)
        # 加载处理后的图片
        self.pix = QPixmap(new_file)
        # 计算并设置图片显示的大小
        pixh = self.pix.height()
        pixw = self.pix.width()
        l = pixh / self.pic_h
        self.pic_w = pixw // l
        self.pixmap.setPixmap(self.pix.scaled(int(self.pic_w), self.pic_h))
        # 将处理后的图片添加回布局
        self.extend_card2_layout.addWidget(self.pixmap)
        # 设置界面大小
        # 假设这里有必要的逻辑
        # 更新图片文件路径显示
        self.extend_drag_edit.setText(new_file)
        # 更新文件目录
        self.file_dir_get()

    def pixmap_get_type(self):
        """
        根据扩展组合框的当前文本，确定图片操作类型，并据此显示或隐藏扩展滑块及其标签。

        此方法处理用户界面的动态变化，根据用户选择的图片操作类型（如旋转、缩小、模糊等），决定是否显示扩展滑块及其标签。
        这是因为某些图片操作类型可能不需要用户输入额外的参数（如旋转），而其他操作（如缩小、模糊）可能需要用户指定程度或量。
        """

        # 获取扩展组合框当前选定的文本
        res = self.extend_combobox.currentText()

        # 如果选定的操作不是旋转、缩小或模糊，则隐藏扩展滑块及其标签
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        if res != "旋转" and res != "缩小" and res != "模糊":
            self.extend_slider.hide()
            self.extend_slider_label.hide()
        else:
            # 否则，显示扩展滑块及其标签
            self.extend_slider.show()
            self.extend_slider_label.show()

        # 保存当前选择的图片操作类型
        self.pixmap_type = res

    def weather_position_get(self):
        """
        获取天气位置信息，并根据该信息更新天气卡片的显示。

        从家天气卡片组合框中获取选定的城市名称。如果名称是中文且不为空，则尝试获取该城市的天气数据，
        并更新天气卡片上的各个标签。如果获取天气数据失败，则将标签设置为未找到的提示。
        """
        # 获取用户在家庭天气卡片组合框中选择的城市名称
        QApplication.processEvents()
        res = self.home_weather_card_combobox.text()
        # 将获取到的城市名称保存为当前的天气位置
        # self.show_info_bar(f"{inspect.stack()[0][3]} -> {res}")
        self.weather_position = res

        # 如果天气位置为空，则不进行后续操作
        if len(self.weather_position) == 0:
            return

        # 如果天气位置的首字符是中文字符
        if '\u4e00' <= self.weather_position[0] <= '\u9fff':
            try:
                # 尝试根据天气位置和城市代码获取天气数据
                data = re_get_weather(self.weather_position, self.city_code)
                # 更新天气卡片上的各个标签，显示天气数据
                self.card2_weather_card_label1.setDes(data[0])
                self.card2_weather_card_label2.setDes(data[1])
                self.card2_weather_card_label3.setDes(data[2])
                self.card2_weather_card_label4.setDes(data[3])
            except Exception as e:
                # 如果获取天气数据失败，将卡片上的标签设置为未找到的提示
                self.card2_weather_card_label1.setDes("未选择")
                self.card2_weather_card_label2.setDes("未找到")
                self.card2_weather_card_label3.setDes("未找到")
                self.card2_weather_card_label4.setDes("未找到")

    def re_get_weather_button(self):
        """
        根据用户选择的城市获取天气信息，并更新界面显示。
        如果天气信息获取成功，更新天气标签的描述；
        如果获取失败，将标签描述设置为“未找到”。
        """
        # 检查是否有城市位置信息，如果没有，则不执行后续操作
        QApplication.processEvents()
        if len(self.weather_position) == 0:
            return
        # 检查城市位置信息是否为中文字符
        if '\u4e00' <= self.weather_position[0] <= '\u9fff':
            try:
                # 使用正则表达式获取天气信息
                data = re_get_weather(self.weather_position, self.city_code)
                # 更新天气标签的描述
                self.card2_weather_card_label1.setDes(data[0])
                self.card2_weather_card_label2.setDes(data[1])
                self.card2_weather_card_label3.setDes(data[2])
                self.card2_weather_card_label4.setDes(data[3])
                # 显示获取成功的提示信息
                self.show_info_bar("获取成功", "success", self.weather_position)
            except Exception as e:
                print(e)
                # 如果获取天气信息失败，更新天气标签的描述为“未找到”
                self.card2_weather_card_label1.setDes("未选择")
                self.card2_weather_card_label2.setDes("未找到")
                self.card2_weather_card_label3.setDes("未找到")
                self.card2_weather_card_label4.setDes("未找到")
                # 显示获取失败的提示信息
                self.show_info_bar("获取失败", "error", self.weather_position)

    def update_slider_label(self):
        """
        更新滑块标签的文本，显示当前滑块的值（以百分比形式）。
        """
        try:
            slider_value = self.extend_slider.value()
            if slider_value is not None and slider_value >= 0:
                percent_value = slider_value / 100
                self.extend_slider_label.setText(f"{slider_value}%")  # 直接使用数值，避免额外的字符串拼接
                self.extend_slider_value = percent_value
            else:
                # 处理异常值，例如设置为0或显示错误信息
                self.extend_slider_label.setText("Invalid Value")
                self.extend_slider_value = None
        except Exception as e:
            # 异常处理逻辑，例如记录日志或显示错误信息
            print(f"An error occurred: {e}")
            self.extend_slider_label.setText("Error")
            self.extend_slider_value = None

    def extend_get_slider(self):
        """
        检查滑块值是否已改变并更新滑块标签。此方法应由滑块值改变的信号触发。
        """
        # 由于这个方法现在假设它只在滑块值改变时被调用，
        # 因此不需要每次调用时都重新计算百分比。
        self.update_slider_label()


if __name__ == '__main__':
    os.environ['QT_SCALE_FACTOR'] = str(1)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()