from urllib.parse import urlencode
import pymongo
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

base_url = 'https://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUV=00B501F0756781125B6B9828AFDBC811; GOTO=Af12468-0057; IPLOC=CN1100; SUID=128167752320940A000000005B70DE71; usid=kER8BfZiwGPxyBis; ABTEST=2|1550724180|v1; weixinIndexVisited=1; PHPSESSID=3iiqpfp3a1k4rvluthkjn7kmg3; JSESSIONID=aaaC0cxN3ffIoetZPD6Hw; ppinf=5|1550724371|1551933971|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1NDolRTQlQkQlQTAlRTUlQTUlQkQlRTQlQjglQjYlRTYlODglOTElRTUlQTclOTMlRTUlQUUlOEJ8Y3J0OjEwOjE1NTA3MjQzNzF8cmVmbmljazo1NDolRTQlQkQlQTAlRTUlQTUlQkQlRTQlQjglQjYlRTYlODglOTElRTUlQTclOTMlRTUlQUUlOEJ8dXNlcmlkOjQ0Om85dDJsdUtDeWt3ZzFIS2NhTFk2SUdoc3NIUGtAd2VpeGluLnNvaHUuY29tfA; pprdig=QNkURIEpUvxkp5riP4MMWFc5ucDVIC08ne1Na8vjwMZb2i_0b6lT9oAtFA4X68bN2gi0dQHYn2B3rPP5wewi77bcW7WX5vdjLTrQz1WCWMxYeX5MlROuZJIgUTX5LMCQsoLYbooqTjI1PmH9TADOOo0SizU_pJ0Qinkpgl-EjPk; sgid=25-39405681-AVxuLRPxTAiaBA3mheb76LYA; sct=3; SNUID=42CA2B3E4B4ECE2AE09287394C3CA2FA; ppmdig=15507320940000006b7eb013d987a23a0005f8a4a3d36863',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}

proxy = None


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying count', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too many counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Useing Proxy', proxy)
                get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keywords, page):
    data = {
        'query': keywords,
        'type': 2,
        'page': page,
        'ie ': 'utf8'
    }
    queries = urlencode(data)
    url = base_url+queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content ').text()
    date = doc('#publish_time').text()
    nickname = doc('#js_name').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    images = doc('#js_content > p > img').items()
    imglist = []
    for image in images:
        if image.attr('data-before-oversubscription-url'):
            imglist.append(image.attr('data-before-oversubscription-url'))
        if image.attr('src'):
            imglist.append(image.attr('src'))
    return {
        'title': title,
        'content': content,
        'date': date,
        'nickname': nickname,
        'wechat': wechat,
        'imglist': imglist
    }


def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Monogo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(5):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                # print('aaa', article_url)
                detail = get_detail(article_url)
                if detail:
                    article_data = parse_detail(detail)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()
