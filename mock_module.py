if __name__ == '__main__':
    from module.browser_mng import browserManage
    from module.amazon_login_automation import amazonLoginAutomation
    import time

    driver = browserManage().get_driver()
    amazonLoginAutomation().execute(driver=driver)
    # 注文履歴画面へ
    order_history = driver.find_element_by_id('nav-orders')
    order_history.click()
    time.sleep(2)
    period = '2021年'
    period_links = driver.find_element_by_class_name('a-dropdown-prompt')
    period_links.click()
    period_links = driver.find_element_by_link_text(period)
    period_links.click()


