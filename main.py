from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

datetime = datetime.now()
counter = 0

# импортируем переменные из dotenv
load_dotenv()

def sync_work():
    # открыть соединение
    with sync_playwright() as p:
        # инициализация браузера (с открытием браузера и задержкой в 10 секунд)
        browser = p.chromium.launch(headless=True, slow_mo=1000)
        # установить локаль на ru
        context = browser.new_context(locale="ru-RU")
        # инициализация страницы
        page = context.new_page()
        # переход по url адресу:
        page.goto('https://google.com/')
        # нажать на кнопку
        #page.get_by_role("button", name="Принять все").click()
        # декларируеми функцию создания скриншотов
        def take_screenshot():
            global counter
            global datetime
            datetime = datetime.now()
            now = datetime.strftime('%m-%d-%Y-%H-%M-%S')
            page.screenshot(path='./screenshots/test-' + str(now) + '-' + str(counter) + '.png')
            counter = counter + 1
        take_screenshot()
        # заполнть поле и выполнить поиск
        page.get_by_label("Найти").fill("makima cosplay"); page.get_by_label("Найти").press("Enter")
        # еще один скриншот
        take_screenshot()
        # закрыть браузер
        browser.close()


# отправка статуса на веб-сервер

class APIResult():
    try:
        sync_work()
        if True:
            print("All Works!")
            data = [{"status": "success"}]
            response = requests.post(os.getenv('URL'), json=data)
            print("Status Code", response.status_code)
            print("JSON Response ", response.json())
    except (RuntimeError, TypeError, NameError):
            data = [{"status": "check failed"}]
            response = requests.post(os.getenv('URL'), json=data)
            print("Check failed!")

