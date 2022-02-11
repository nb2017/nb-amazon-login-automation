import time
import json
from module.browser_mng import browserManage

class amazonLoginAutomation:
    login_setting = None
    def __init__(self) -> None:
        json_open = open('settings/amazon_login_setting.json', 'r')
        self.login_setting = json.load(json_open)
    def execute(self, driver = None):
        if driver is None:
            driver = browserManage().get_driver()
        #画面遷移
        driver.get('https://www.amazon.co.jp/')

        #ログイン画面に遷移
        mailad = driver.find_element_by_id('nav-link-accountList')
        mailad.click()

        # ログインIDを入力
        login_id = driver.find_element_by_id("ap_email")
        login_id.send_keys(self.login_setting['login_email'])

        #「次に進む」をクリック
        nextb = driver.find_element_by_class_name("a-button-input")
        nextb.click()
        time.sleep(1)

        #パスワードを入力
        password = driver.find_element_by_name("password")
        password.send_keys(self.login_setting['login_password'])

        #「ログイン」をクリック
        nextb = driver.find_element_by_id("signInSubmit")
        nextb.click()
        time.sleep(1)
