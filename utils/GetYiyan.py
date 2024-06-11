import requests


def get_yiyan() -> str:
    random_pic = "https://tenapi.cn/v2/yiyan"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    try:
        req = requests.get(random_pic, headers=headers)
        return req.text
    except  Exception as e:
        print(e)


if __name__ == "__main__":
    get_yiyan()
