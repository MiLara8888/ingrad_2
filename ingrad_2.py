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
        launch()
        global spisok
        print('выполняюсь')
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
                if re.match(r'\/projects\/\w+\/select\/commercial\/all',
                            str(i.get('href'))) and 'https://www.ingrad.ru' + str(i.get('href')) not in spisok:
                    spisok.append('https://www.ingrad.ru' + str(i.get('href')))
                    bot.send_message(487422659, 'https://www.ingrad.ru' + str(i.get('href')))
            except:
                bot.send_message(487422659, 'Бот сломался')
                time.sleep(50)
                continue

        func()
        close(launch())
    except:
        close(launch())
        time.sleep(50)
        func()


func()
