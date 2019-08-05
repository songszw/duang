import requests
import time
from bs4 import BeautifulSoup

# proxies = {
#   "http": "http://dongtaiwang.com:45671",
#   "https": "http://dongtaiwang.com:45671"
# }
# headers = {
#   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
# }

def get_image(url):

  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
  }
  # url = 'http://ip.tool.chinaz.com/'
  proxies = {
    # "https": "https://222.189.144.147:9999"
      "http": "http://183.128.167.248:8118"
  }
  response = requests.get(url, headers=headers, proxies=proxies)
  if response.status_code == 200:
    return response.content
  else:
    print(response.status_code, proxies)


def save_img(img, page):
  with open('container/'+str(page)+'.png', 'wb') as f:
    f.write(img)
    f.close()
    print('文件'+str(page)+'保存成功')

def main(pages):
  url = 'https://www.gujiguan.com/showpic.aspx?book=Uz6ulhNWhZY=&page='+str(pages)
  img = get_image(url)
  save_img(img, pages)

if __name__ == '__main__':
  for i in range(1):
    main(i + 1)

# import requests
# from lxml import etree

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
# }
# url = 'http://ip.tool.chinaz.com/'
# proxies = {
#     "https": "https://111.226.188.146:8010"
# }

# wb_data = requests.get(url=url, headers=headers, proxies=proxies)
# content = etree.HTML(wb_data.text)
# print(content.xpath('//*[@id="rightinfo"]/dl/dd[1]/text()')[0])
