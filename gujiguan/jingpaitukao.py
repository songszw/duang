import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.gujiguan.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#Text1'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#fm > span.s-btn-w'))
        )

        input.send_keys('經脈圖考')
        submit.click()
        into_book = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#DataList1 > tbody > tr > td > table > tbody > tr > td.sreach_result > a:nth-child(2)'))
        )
        into_book.click()

    except TimeoutException as e:
        search()


def main():
    search()


if __name__ == '__main__':
    main()
