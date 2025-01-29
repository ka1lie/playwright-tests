from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
import json

datetime = datetime.now()
counter = 0
load_dotenv()

with open('checker.json', 'r') as file:
    data = json.load(file)
    browser_type = data['browser']
    headless = bool(data['headless'])
    slow_mo = int(data['slow_mo'])
    locale = data['locale']
    start_url = data['start_url']


def sync_work():

    with sync_playwright() as p:

        if browser_type == 'chromium':
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        elif browser_type == 'firefox':
            browser = p.firefox.launch(headless=headless, slow_mo=slow_mo)
        elif browser_type == 'webkit':
            browser = p.webkit.launch(headless=headless, slow_mo=slow_mo)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
            sys.exit(0)

        context = browser.new_context(locale=locale)
        page = context.new_page()
        page.goto(start_url)

        def take_screenshot():
                global counter
                global datetime
                datetime = datetime.now()
                now = datetime.strftime('%m-%d-%Y-%H-%M-%S')
                page.screenshot(path='./screenshots/test-' + str(now) + '-' + str(counter) + '.png')
                counter = counter + 1

        take_screenshot()

        if not data['auth']:
             print("Auth is empty")
        else:
             auth_info = data['auth'][0]  
             login = auth_info['login']
             password = auth_info['encrypted_password']
             print(login)
             print(password)


        browser.close()
    

class APIResult():
    try:
        sync_work()
        if True:
            print("All Works!")
#            data = [{"status": "success"}]
#            response = requests.post(os.getenv('URL') + "test", json=data)
#            print("Status Code", response.status_code)
#            print("JSON Response ", response.json())
    except:
 #           data = [{"status": "check failed"}]
 #           response = requests.post(os.getenv('URL') + "test", json=data)
            print("Check failed!")
