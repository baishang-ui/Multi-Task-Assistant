# https://blog.csdn.net/Claire_chen_jia/article/details/106281498
import json

import requests


def re_get_weather(city_name: str, city_codew_dir):
    """
    根据城市名称获取天气信息。

    该函数通过城市名称从一个本地JSON文件中查找城市代码，
    然后使用这个城市代码从一个天气API中获取并返回天气预报信息。

    参数:
    city_name (str): 需要获取天气信息的城市名称。
    city_codew_dir (str): 存储城市代码的JSON文件的路径。

    返回:
    list: 包含城市名称、天气情况、最高温度和最低温度的列表。
          如果获取天气信息失败，则返回一个包含"error"的列表。
    """
    # 定义天气API的URL基础部分
    # api地址
    url = 'http://t.weather.sojson.com/api/weather/city/'

    # 打开并读取存储城市代码的JSON文件
    # 读取json文件
    f = open(city_codew_dir, 'rb')

    # 加载JSON文件内容到Python对象
    # 使用json模块的load方法加载json数据，返回一个字典
    cities = json.load(f)

    # 通过城市名称查找并获取城市代码
    # 通过城市的中文获取城市代码
    city = cities.get(city_name)

    # 发起HTTP请求，获取天气信息
    # 网络请求，传入请求api+城市代码
    response = requests.get(url + city)

    # 解析HTTP响应，获取JSON格式的天气数据
    # 将数据以json形式返回，这个d就是返回的json数据
    d = response.json()

    # 检查API调用是否成功
    # 当返回状态码为200，输出天气状况
    if d['status'] == 200:
        # 如果成功，返回城市名称、天气情况、最高温度和最低温度
        return [d["cityInfo"]["city"], d["data"]["forecast"][0]["type"], d["data"]["forecast"][0]["high"][3:],
                d["data"]["forecast"][0]["low"][3:]]
    else:
        # 如果失败，返回一个包含"error"的列表
        return [["error"], ]


if __name__ == '__main__':
    wea = re_get_weather("景德镇", "E:\\Python_project_Pycharm\\EndProject\\resource\\city_to_code.json")
    print(wea)
