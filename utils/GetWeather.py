# https://blog.csdn.net/Claire_chen_jia/article/details/106281498
import requests
from bs4 import BeautifulSoup


def get_info(source):
    # 解决网页乱码，添加'html5lib'，而不是lxml
    if source == "获取失败":
        return "获取失败"
    try:
        soup = BeautifulSoup(source, 'html5lib')  # pip install html5lib
        # 1.进入整体表格
        conMidtab = soup.find('div', class_='conMidtab')
        # 2.进入子表格
        tables = conMidtab.find_all('table')
        # 3.进入每个子表格收集天气信息
        items = []
        for i in tables:
            trs = i.find_all('tr')[2:]
            for i, e in enumerate(trs):
                tds = e.find_all("td")
                city_td = tds[-8]
                city = list(city_td.stripped_strings)[0]
                # 该城市最高气温
                temp_high_td = tds[-5]
                temp_high = list(temp_high_td.stripped_strings)[0]
                # 该城市最低气温
                temp_low_td = tds[-2]
                temp_low = list(temp_low_td.stripped_strings)[0]
                # 该城市天气状况
                weather = tds[-4]
                weather_ = list(weather.stripped_strings)[0]
                # test
                item = [city, weather_, temp_high, temp_low]
                items.append(item)
        return items
    except Exception as e:
        print(e)
        items = [["1", "2", "3", "4"]]
        return items


def get_weather_data():
    info_list = []
    dq_names = ['hb', 'db', 'hd', 'hz', 'hn', 'xb', 'xn', 'gat']
    for dq_name in dq_names:
        url = 'http://www.weather.com.cn/textFC/' + dq_name + '.shtml'
        source = get_source(url)
        info = get_info(source)
        if info == "获取失败":
            return "获取失败"
        info_list += info
    return info_list


def get_source(url):
    try:
        response = requests.get(url, timeout=3)
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        return "获取失败"


if __name__ == '__main__':
    wea = get_weather_data()
    print(wea)
