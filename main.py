from playwright.sync_api import sync_playwright

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
        page.get_by_role("button", name="Принять все").click()
        # сделать скриншот
        page.screenshot(path='./demo.png')
        # заполнть поле и выполнить поиск
        page.get_by_label("Найти").fill("makima cosplay"); page.get_by_label("Найти").press("Enter")
        # еще один скриншот
        page.screenshot(path='./demo1.png')
        browser.close()

try:
    sync_work()
    if True:
        print("All Works!")
except (RuntimeError, TypeError, NameError):
    pass