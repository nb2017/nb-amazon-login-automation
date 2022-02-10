import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class amazonLoginAutomation:
    driver = None
    options = None
    login_setting = None
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.options)
        json_open = open('settings/amazon_login_setting.json', 'r')
        self.login_setting = json.load(json_open)
    def execute(self):
        #画面遷移
        self.driver.get('https://www.amazon.co.jp/')

        #ログイン画面に遷移
        mailad = self.driver.find_element_by_id('nav-link-accountList')
        mailad.click()

        # ログインIDを入力
        login_id = self.driver.find_element_by_id("ap_email")
        login_id.send_keys(self.login_setting['login_email'])

        # 「次に進む」をクリック
        nextb = self.driver.find_element_by_class_name("a-button-input")
        nextb.click()
        time.sleep(1)

        # パスワードを入力
        password = self.driver.find_element_by_name("password")
        password.send_keys(self.login_setting['login_password'])

        # 「ログイン」をクリック
        nextb = self.driver.find_element_by_id("signInSubmit")
        nextb.click()
        time.sleep(1)
