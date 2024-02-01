import time
import json
from module.browser_mng import browserManage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class amazonLoginAutomation:
    """
    Amazonへの自動ログインを行うクラス
    """
    login_setting = None
    def __init__(self) -> None:
        """
        コンストラクタ
        """
        json_open = open('settings/amazon_login_setting.json', 'r')
        self.login_setting = json.load(json_open)
    def execute(self, driver = None):
        """
        自動ログインを実行する
        Parameters
        ----------
        driver : browserManage
            Chrome Webドライバ

        Returns
        -------
        なし
        """
        if driver is None:
            driver = browserManage().get_driver()
        #画面遷移
        driver.get('https://www.amazon.co.jp/')

        #ログイン画面に遷移
        mailad = driver.find_element(By.ID, 'nav-link-accountList-nav-line-1')
        actions = ActionChains(driver=driver)
        actions.move_to_element(mailad)
        mailad.click()

        # # ログインIDを入力
        login_id = driver.find_element(By.ID, "ap_email")
        login_id.send_keys(self.login_setting['login_email'])
        time.sleep(1)

        # #「次に進む」をクリック
        nextb = driver.find_element(By.ID, "continue")
        nextb.click()
        time.sleep(1)

        # #パスワードを入力
        password = driver.find_element(By.NAME, "password")
        password.send_keys(self.login_setting['login_password'])
        time.sleep(1)

        # #「ログイン」をクリック
        nextb = driver.find_element(By.ID, "auth-signin-button")
        nextb.click()
        time.sleep(1)
