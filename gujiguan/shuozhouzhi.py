# import requests
# import os
# url="https://www.gujiguan.com/showpic.aspx?book=Avoo8GCdf1I=&page=1"
# try:
#     r=requests.get(url)
#     with open('01.png','wb')as f:
#         f.write(r.content)
#         f.close()
#         print("文件保存成功")
#
# except:
#     print("爬取失败")

import requests
import time

def get_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content


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
        time.sleep(1)

