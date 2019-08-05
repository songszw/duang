import requests
import time
from requests.exceptions import ConnectionError

proxy_pool_url = 'http://localhost:5000/get'


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_image(url):
    proxies = {
        'http': 'http://'+get_proxy()
    }
    response = requests.get(url, proxies=proxies)
    if response.status_code == 200:
        return response.content
    print(response.status_code)


def save_img(img,pages):
    with open(str(pages)+'.png', 'wb') as f:
        f.write(img)
        f.close()
        print('文件'+str(pages)+'保存成功')


def main(pages):
    url = 'https://www.gujiguan.com/showpic.aspx?book=Avoo8GCdf1I=&page='+str(pages)
    img = get_image(url)
    save_img(img, pages)


if __name__ == '__main__':
    for i in range(513):
        main(i+1)

