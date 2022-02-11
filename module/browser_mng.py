from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

class browserManage:
    driver = None
    options = None
    def __init__(self) -> None:
        self.options = Options()
        settings = {"recentDestinations": [{"id": "Save as PDF",
                                            "origin": "local",
                                            "account": ""}],
                    "selectedDestinationId": "Save as PDF", 
                    "version": 2}
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
        self.options.add_experimental_option('prefs', prefs)
        self.options.add_argument('--kiosk-printing')
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.options)

    def get_driver(self):
        return self.driver