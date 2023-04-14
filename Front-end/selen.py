import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.safari import SafariDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from security import COOKIES

TAG = "tag name"
XPATH = "xpath"
CLASS = "class name"


class Selen:

    def __init__(self, wd="Chrome", headless=False):

        self.elem = None
        if wd == "Chrome":
            opts = webdriver.ChromeOptions()
            opts.add_argument('--disable-blink-features=AutomationControlled')
            if headless:
                opts.add_argument('headless')
            opts.add_argument('window-size=1600x2600')

            self.WD = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

        elif wd == "Firefox":
            opts = webdriver.FirefoxOptions()
            opts.add_argument('--start-maximized')
            opts.add_argument('--disable-extensions')
            self.WD = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=opts)

        elif wd == "Edge":
            opts = webdriver.EdgeOptions()
            opts.use_chromium = True
            opts.binary_location = '/opt/microsoft/msedge/msedge'
            opts.add_argument('--start-maximized')
            self.WD = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=opts)

        self.wd_name = wd
        self.WD.maximize_window()
        self.WD.act_chain = ActionChains(self)
        self.WDW = WebDriverWait(self.WD, 10)
        self.url = ""
        self.elem = self.WD
        self.assert_ok = True
        self.print_ok = True

    def add_cookies(self):
        for cookie in COOKIES[self.wd_name]:
            self.WD.execute_cdp_cmd('Network.setCookie', cookie)
            # self.WD.add_cookie(cookie)

    def print(self, *args, **kwargs):
        if self.print_ok:
            print(*args, **kwargs)

    def assertion(self):
        if self.assert_ok:
            assert False

    def click_to(self, *args):
        self.find(*args).click()
        self.print("Clicked element:", self.elem)

    def wait_click_to(self, *args):
        self.wait_find(*args).click()
        self.print("Clicked element:", self.elem)

    def wait_find(self, *args):
        self.print("Looking for :", args)
        try:
            elem = self.WDW.until(EC.presence_of_element_located(args[0]))
        except NoSuchElementException:
            print("Element not found!")
            self.assertion()
            return None
        except TimeoutException:
            print("Command timed out!")
            self.assertion()
            return None
        print(args[1:])
        if args[1:]:
            elem = self.find_in(elem, *args[1:])

        self.elem = elem
        return elem

    def find(self, *args):
        elem = self.WD
        return self.find_in(elem, *args)

    def find_in(self, elem, *args):
        for by in args:
            try:
                print(by)
                elem = elem.find_element(*by)
            except NoSuchElementException:
                print("Element not found!")
                self.assertion()
                return None
        self.elem = elem
        return elem

    def send_text(self, text):
        self.elem.click()
        self.elem.clear()
        self.elem.send_keys(text)
        self.print("Text sent:", text)

    def wait_text_to(self, text: str, *args):
        self.elem = self.wait_find(*args)
        self.send_text(text)

    def text_to(self, text: str, *args):
        self.elem = self.find(*args)
        self.send_text(text)

    def checker(self, got, expect, message):
        if self.assert_ok:
            assert got == expect, f"!!! Wrong {message}"
        else:
            try:
                assert got == expect, message
            except AssertionError:
                print("!!! Wrong", message)
                print("Got:", got)
                print("Expected:", expect)
                return

        if self.print_ok:
            self.print("Checked:", message, "is OK")

    def check_title(self, title):
        self.checker(self.WD.title, title, f"Title at: {self.WD.current_url}")

    def check_url(self, url):
        self.checker(self.WD.current_url, url, "URL")

    def check_text(self, text, *args):
        if args:
            elem = self.find(*args)
        else:
            elem = self.elem.find_element("tag name", "html")

        self.checker(elem.text, text, f"Text at elements: {elem}")

    def check_wait_text(self, text, *args):
        if args:
            elem = self.wait_find(*args)
        else:
            elem = self.elem

        self.checker(elem.text, text, f"Text at waited elements: {elem}")

    def save_cookies_to_file(self, file_name):
        if self.wd_name in COOKIES:
            self.print("Cookies found")
            return
        COOKIES[self.wd_name] = self.WD.get_cookies()
        with open(file_name, 'a') as f:
            f.write(f'COOKIES = {COOKIES}\n')
            self.print("Cookies saved")

    # def get_elem(self, find_func):
    #     self.WD.get(self.url + self.link)
    #     self.elem = find_func()
    #     return self.elem
    #
    # def get_elems(self, find_func):
    #     self.elems = []
    #     for link in self.links:
    #         # self.get(self.url + link)
    #         self.elems.extend(find_func())
    #         elems = find_func()
    #         print(len(elems))
    #         time.sleep(1)
    #         break
    #         # print(self.elems)
    #     return self.elems
    #
    # def get_hrefs(self, find_func, norm_func=normalize_link):
    #     self.get_elems(find_func)
    #     self.links = sorted([*set([norm_func(elem.get_attribute('href')) for elem in self.elems])])
    #     return self.links
    #
    # @Timer
    # def get_data(self, find_func):
    #     for link in self.links:
    #         self.get(link)
    #         self.data[link] = find_func()
    #
    # def save_to_json(self, file_name):
    #     with open(file_name, 'w', encoding='utf-8') as f:
    #         json.dump(self.data, f, indent=4)


if __name__ == '__main__':
    time.sleep(15)
