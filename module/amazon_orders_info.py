import time
import os
import json
import shutil

from module.browser_mng import browserManage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class amazonOrdersInfo:
    """
    Amazonの注文履歴から領収証PDFをダウンロードをサポートするクラス
    """
    # 注文履歴PDFダウンロード設定
    amazon_orders_pdf_setting = None
    def __init__(self) -> None:
        """
        amazonOrdersInfoクラスのコンストラクタ
        """
        json_open = open('settings/amazon_orders_pdf_setting.json', 'r')
        self.amazon_orders_pdf_setting = json.load(json_open)
    
    def execute(self, driver = None):
        """
        Amazonの注文履歴ページから対象の期間の注文情報から領収証PDFを指定のフォルダにダウンロードする
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

        for period in self.amazon_orders_pdf_setting['periods']:
            # 注文履歴画面へ
            order_history = driver.find_element(By.ID, 'nav-orders')
            order_history.click()
            time.sleep(2)
            # 対象の期間をセットする
            self.changePeriods(period, driver=driver)
            all_page_num = int(driver.find_element(By.CLASS_NAME, 'num-orders').text.replace('件',''))
            print(f'処理予定ページ数：{all_page_num}')
            # すべてのページで行う
            for page_num in range(all_page_num):

                main_handle = driver.current_window_handle
                receipt_links = driver.find_elements(By.LINK_TEXT, '領収書等')
                # 1ページないのすべての領収書で行う
                for receipt_link in receipt_links:
                    try:
                        receipt_link.click()
                        time.sleep(1)
                        receipt_purchase_link = driver.find_element(By.LINK_TEXT, '領収書／購入明細書')
                        # 商品の注文履歴ページに遷移
                        self.openOrderInfoPage(driver=driver, receipt_purchase_link=receipt_purchase_link)
                        # PDFダウンロード
                        self.pdfDownload(driver=driver)
                        time.sleep(1)
                        driver.close()
                        driver.switch_to.window(main_handle)
                    except:
                        pass

                try:
                    # 次のページに遷移
                    self.changeNextPage(driver=driver)
                except:
                    break

        driver.quit()

    def changePeriods(self, period, driver=None):
        """
        対象とする注文履歴の期間を変更する
        Parameters
        ----------
        period : int
            対象の期間 YYYY 例:2022
        driver : browserManage
            Chrome Webドライバ

        Returns
        -------
        なし
        """
        if driver is None:
            driver = browserManage().get_driver()
        if F'{str(period)}年':
            period_links = driver.find_element(By.CLASS_NAME, 'a-dropdown-prompt')
            period_links.click()
            period_links = driver.find_element(By.LINK_TEXT, F'{str(period)}年')
            period_links.click()

    def openOrderInfoPage(self, driver = None, receipt_purchase_link = None):
        """
        注文履歴ページを開く
        Parameters
        ----------
        driver : browserManage
            Chrome Webドライバ
        receipt_purchase_link : WebElement
            注文履歴ページのリンクエレメント

        Returns
        -------
        なし
        """
        if driver is None:
            driver = browserManage().get_driver()
        if receipt_purchase_link is None:
            receipt_purchase_link = driver.find_element(By.LINK_TEXT, '領収書／購入明細書')

        # クリック前のハンドルリスト
        handles_before = driver.window_handles
        # 新しいタブで開く
        actions = ActionChains(driver)
        actions.key_down(Keys.COMMAND)
        actions.click(receipt_purchase_link)
        actions.perform()
        # 新しいタブが開くまで最大30秒待機
        WebDriverWait(driver, 30).until(lambda a: len(driver.window_handles) > len(handles_before))
        # クリック後のハンドルリスト
        handles_after = driver.window_handles

        # ハンドルリストの差分
        handle_new = list(set(handles_after) - set(handles_before))
        # 新しいタブに移動
        driver.switch_to.window(handle_new[0]) 
        actions.key_down(Keys.COMMAND)
    
    def pdfDownload(self, driver = None):
        """
        対象とする注文履歴の期間を変更する
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
        # pdf化
        driver.execute_script('window.print();')

        # pdf化したものをダウンロードフォルダから指定フォルダに名前を変更して保存する

        elem = driver.find_element(By.CLASS_NAME, 'h1')
        new_filename = elem.text + '.pdf'# 新しいファイル名
        try:
            timestamp_now = time.time() # 現在時刻
            # ダウンロードフォルダを走査
            for (dirpath, dirnames, filenames) in os.walk(self.amazon_orders_pdf_setting['download_path']):
                for filename in filenames:
                    if filename.lower().endswith(('.pdf')):
                        full_path = os.path.join(self.amazon_orders_pdf_setting['download_path'], filename)
                        timestamp_file = os.path.getmtime(full_path) # ファイルの時間
                        # 3秒以内に生成されたpdfを移動する
                        if (timestamp_now - timestamp_file) < 3:
                            shutil.move(full_path, self.amazon_orders_pdf_setting['save_path'])
                            print(f'{full_path} is moved to {self.amazon_orders_pdf_setting['save_path']}')
        except Exception as e:
            print(f'ERROR {e}')

    def changeNextPage(self, driver = None):
        """
        次のページに遷移する
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
        try:
            # 次へのボタンが押せなくなった時点で終了
            driver.find_element(By.CLASS_NAME, 'a-last').find_element(By.TAG_NAME, 'a')
            driver.find_element(By.CLASS_NAME, 'a-last').click()
            driver.switch_to.window(driver.window_handles[-1])
        except:
            raise

