import time
import os
import json

from module.browser_mng import browserManage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class amazonOrdersInfo:
    def __init__(self) -> None:
        pass
    def execute(self, driver = None):
        if driver is None:
            driver = browserManage().get_driver()
        json_open = open('settings/amazon_orders_pdf_setting.json', 'r')
        amazon_orders_pdf_setting = json.load(json_open)

        # 注文履歴画面へ
        order_history = driver.find_element_by_id('nav-orders')
        order_history.click()
        time.sleep(2)

        # すべてのページで行う
        while True:

            main_handle = driver.current_window_handle
            receipt_links = driver.find_elements_by_link_text('領収書等')
            # 1ページないのすべての領収書で行う
            for receipt_link in receipt_links:
                try:
                    receipt_link.click()
                    time.sleep(1)
                    receipt_purchase_link = driver.find_element_by_link_text('領収書／購入明細書')

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
        
                    # pdf化
                    driver.execute_script('window.print();')

                    # pdf化したものをダウンロードフォルダから指定フォルダに名前を変更して保存する

                    new_filename = driver.find_element_by_class_name('h1').text + '.pdf'# 新しいファイル名
                    timestamp_now = time.time() # 現在時刻
                    # ダウンロードフォルダを走査
                    for (dirpath, dirnames, filenames) in os.walk(amazon_orders_pdf_setting['download_path']):
                        for filename in filenames:
                            if filename.lower().endswith(('.pdf')):
                                full_path = os.path.join(amazon_orders_pdf_setting['download_path'], filename)
                                timestamp_file = os.path.getmtime(full_path) # ファイルの時間
                                # 3秒以内に生成されたpdfを移動する
                                if (timestamp_now - timestamp_file) < 3: 
                                    full_new_path = os.path.join(amazon_orders_pdf_setting['save_path'], new_filename)
                                    os.rename(full_path, full_new_path)
                                    print(full_path+' is moved to '+full_new_path) 
                    time.sleep(1)
                    driver.close()
                    driver.switch_to.window(main_handle)
                except:
                    pass

            # 次へのボタンが押せなくなった時点で終了
            try:
                driver.find_element_by_class_name('a-last').find_element_by_tag_name('a')
                driver.find_element_by_class_name('a-last').click()
                driver.switch_to.window(driver.window_handles[-1])
            except:
                break 

        driver.quit()
