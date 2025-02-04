from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from cryptography.fernet import Fernet
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
             print("Auth is empty, skipping...")
        else:
             print("Start reading auth info...")  
             auth_info = data['auth'][0]  
             login = auth_info['login']
             password = auth_info['encrypted_password']
             login_selector = auth_info['login_selector']
             password_selector = auth_info['password_selector']
             login_button = auth_info['login_button']

             if auth_info['encrypted_password']:
                def password_decryption():
                    key = open("./creds/key", "rb").read() 
                    fernet = Fernet(key)
                    global decPassword
                    decPassword = fernet.decrypt(bytes(password, 'utf-8')).decode()
                password_decryption()    


             def define_fill(page, selector, value):
                    if selector.startswith('text='):
                        page.get_by_text(selector.replace('text=', '')).fill(value)
                    elif selector.startswith('label='):
                        page.get_by_label(selector.replace('label=', '')).fill(value)
                    elif selector.startswith('placeholder='):
                        page.get_by_placeholder(selector.replace('placeholder=', '')).fill(value)

             def define_click(page, selector):
                    if selector.startswith('text='):
                        page.get_by_text(selector.replace('text=', '')).clicl()
                    elif selector.startswith('label='):
                        page.get_by_label(selector.replace('label=', '')).click()
                    elif selector.startswith('placeholder='):
                        page.get_by_placeholder(selector.replace('placeholder=', '')).click()

             def fill_login_credentials(page, login_selector, login, password_selector, password, login_button):
                    # Fill login field
                    define_fill(page, login_selector, login)
                    print("Login is filled")
                    
                    # Fill password field
                    define_fill(page, password_selector, password)
                    print("Password is filled")

                    define_click(page, login_button)
                    print("Button is clicked")

             fill_login_credentials()
             take_screenshot()

#             if login_selector.startswith('text='):
       #           print(login_selector.replace('text=', ''))
#                  page.get_by_text(login_selector.replace('text=', '')).fill(login)
#             if login_selector.startswith('label='):
#                  page.get_by_label(login_selector.replace('label=', '')).fill(login)
#            if login_selector.startswith('placeholder='):
#                  page.get_by_placeholder(login_selector.replace('placeholder=', '')).fill(login)

#             if password_selector.startswith('text='):
#                  page.get_by_text(password_selector.replace('text=', '')).fill(password)
#             if password_selector.startswith('label='):
#                  page.get_by_label(password_selector.replace('label=', '')).fill(password)
#             if password_selector.startswith('placeholder='):
#                  page.get_by_placeholder(password_selector.replace('placeholder=', '')).fill(password)

            
                

# необходимые конструкции - placeholder, text, button, label, fill, click

        steps = data['steps'][0]

        for i in range(len(data['steps'][0])):
#             if 
#             print(data['steps'][1])
             print(i)
#             print(login)
#             print(password)


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
