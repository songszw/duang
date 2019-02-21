import requests
import time


def get_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(response.status_code)

def save_img(img, page):
    with open('container/'+str(page)+'.png', 'wb') as f:
        f.write(img)
        f.close()
        print('文件'+str(page)+'保存成功')


def main(pages):
    url = 'https://www.gujiguan.com/showpic.aspx?book=FWn%2BBe6cur0=&page='+str(pages)
    img = get_image(url)
    save_img(img, pages)


if __name__ == '__main__':
    for i in range(218):
        main(i + 1)

