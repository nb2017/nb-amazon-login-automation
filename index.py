from module.amazon_login_automation import amazonLoginAutomation
from module.amazon_orders_info import amazonOrdersInfo
from module.browser_mng import browserManage

if __name__ == "__main__":
    browser = browserManage().get_driver()
    amazonLoginAutomation().execute(browser)
    amazonOrdersInfo().execute(browser)
