from module.amazon_login_automation import amazonLoginAutomation
from module.amazon_orders_info import amazonOrdersInfo
from module.browser_mng import browserManage

if __name__ == "__main__":
    driver = browserManage().get_driver()
    amazonLoginAutomation().execute(driver=driver)
    amazonOrdersInfo().execute(driver=driver)
    driver.quit()
