from selenium import webdriver
from selenium import webdriver

class WebDriverManager:
    def __init__(self, msg_manager):
        self.__driver = self.__init_driver()
        self.msg_manager = msg_manager

    def __init_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-javascript")
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        options.page_load_strategy = 'eager'
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--remote-debugging-port=0")

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(640, 480)
        return driver

    def get_driver(self):
        return self.__driver

    def close_driver(self):
        try:
            if self.__driver:
                self.__driver.close()
                self.__driver.quit()
        except Exception as e:
            self.msg_manager.show_message('error_clos_driver', e)

    def next_or_exit(self):
        if self.__driver and self.__driver.service.process:
            self.close_driver()

        while True:
            self.msg_manager.show_message('continue_or_exit', inline=True)
            NoE = input("").strip().lower()

            if NoE == "y" or NoE == "н":
                return True
            elif NoE == "n" or NoE == "т":
                self.msg_manager.show_message('program_complete')
                return False
            else:
                self.msg_manager.show_message('invalid_input')
