from playwright.sync_api import sync_playwright
from datetime import datetime

datetime = datetime.now()
now = datetime.strftime('%m-%d-%Y-%H-%M-%S')

counter = 0

def sync_work():
    # открыть соединение
    with sync_playwright() as p:
        # инициализация браузера (с открытием браузера и задержкой в 10 секунд)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        # инициализация страницы
        page = browser.new_page()
        # переход по url адресу:
        page.goto('https://google.com/')
        # нажать на кнопку
        #page.get_by_role("button", name="Принять все").click()
        # декларируеми функцию создания скриншотов
        def take_screenshot():
            global counter
            page.screenshot(path='./screenshots/test-' + str(now) + '-' + str(counter) + '.png')
            counter = counter + 1
        take_screenshot()
        # заполнть поле и выполнить поиск
        page.get_by_label("Найти").fill("makima cosplay"); page.get_by_label("Найти").press("Enter")
        # еще один скриншот
        take_screenshot()
        # закрыть браузер
        browser.close()


# сделал отдельную функцию result потому что планирую ее отправлять на web-server чтобы проверять что у нас
# все гуд по API

class APIResult():
    try:
        sync_work()
        if True:
            print("All Works!")
    except (RuntimeError, TypeError, NameError):
        pass

result = APIResult()