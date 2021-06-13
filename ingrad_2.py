from requests_html import HTMLSession
import ssl
from bs4 import BeautifulSoup
import re
import urllib3
import telebot
import os
import time
import pyppdf.patch_pyppeteer
import pyppeteer

urllib3.disable_warnings()
spisok = []
token = '1888887403:AAGE01kaCBaUP9TFvzIBqDxVasZbI8v01lI'  # MYtestbot
bot = telebot.TeleBot(token)
exec_path = os.environ.get("GOOGLE_CHROME_SHIM", None)


def launch():
    browser = pyppeteer.launch(executablePath=exec_path,
                               args=[
                                   "--no-sandbox",
                                   # "--single-process",
                                   "--disable-dev-shm-usage",
                                   "--disable-gpu",
                                   "--no-zygote",
                               ], )
    return browser


def close(browser):
    return browser.close()


def func():

    try:

        result_spisok = []
        url1 = 'https://www.ingrad.ru/commercial/'
        headers = {'accept': '/',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
        session = HTMLSession(verify=False)
        context = ssl.SSLContext()
        r = session.get(url=url1, headers=headers, verify=False)
        r.html.render(timeout=1000)
        content = r.html.html
        time.sleep(10)
        soup = BeautifulSoup(content, "lxml")
        for i in soup.find_all(class_='overlink'):
            try:
                if re.match(r'\/projects\/\w+\/select\/commercial\/all', str(i.get('href'))):
                    result_spisok.append('https://www.ingrad.ru' + str(i.get('href')))
            except:
                time.sleep(50)
                continue
        session.close()
        return result_spisok
    except:
        return []
while True:
    launch()
    res=func()
    for i in res:
        if i not in spisok:
            bot.send_message(487422659,i)
    if len(res)!=0:
        spisok=res
    print('проверка завершилась')
    close(launch())
    time.sleep(100)
