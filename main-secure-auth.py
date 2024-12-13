from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from cryptography.fernet import Fernet

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
        context = browser.new_context(locale="en-EN")
        # инициализация страницы
        page = context.new_page()
        # переход по url адресу:
        page.goto('http://grafana.ka1lie.online/login')
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

        def password_decryption():
            encPassword = bytes(open("./creds/test", "r").read(), "")
            key = open("./creds/key", "r").read()
            print(encPassword)
            print(key) 


            fernet = Fernet(key)
            decPassword = fernet.decrypt(encPassword).decode()
            print("decrypted string: ", str(decPassword))

        password_decryption()

        page.get_by_placeholder("email or username").fill("admin")
        #page.get_by_placeholder("password").fill(password_decryption())
        take_screenshot()
        page.get_by_text("Log in").click()        

        # тут мы ожидаем что селектор прогрузится
        page.wait_for_selector('text=Welcome to Grafana')
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
    except:
            data = [{"status": "check failed"}]
            response = requests.post(os.getenv('URL'), json=data)
            print("Check failed!")

