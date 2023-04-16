import time
from random import uniform

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.safari import SafariDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from security import COOKIES

ID = "id"
TAG = "tag name"
XPATH = "xpath"
CLASS = "class name"
NAME = "name"
LINK = "link text"
PART_LINK = "partial link text"
CSS = "css selector"


class Selen:

    def __init__(self, wd="Chrome", headless=False):

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

        self.elems = []
        self.elem = WebElement
        self.wd_name = wd
        self.WD.maximize_window()
        self.WD.act_chain = ActionChains(self)
        self.WDW = WebDriverWait(self.WD, 10)
        self.url = ""
        self.assert_ok = True
        self.print_ok = True

    def add_cookies(self):
        for cookie in COOKIES[self.wd_name]:
            self.WD.execute_cdp_cmd('Network.setCookie', cookie)
            # self.WD.add_cookie(cookie)

    def print(self, *args, **kwargs):
        if self.print_ok:
            print(*args, **kwargs)

    def sleep(self, seconds, finish=None):
        if finish is None:
            time.sleep(seconds)
            return self

        time.sleep(uniform(seconds, finish))
        return self

    def assertion(self, message=''):
        print("!!!", message)
        if self.assert_ok:
            assert False, message

    def click(self):
        self.elem.click()
        self.print("Clicked element:", self.elem)
        return self

    def Wait(self, *args):
        args = self.__args_normalizer(args)
        self.print("Waiting and Looking for :", args)
        try:
            elem = self.WDW.until(EC.presence_of_element_located(args[0]))
        except NoSuchElementException:
            self.assertion(f"Element not found: {args[0]}")
            return None
        except TimeoutException:
            print("Command timed out!")
            self.assertion(f"Element not found: {args[0]}")
            return None
        self.print("Wait Element found", args[0])

        self.elem = elem
        self.elems = [self.elem]
        if args[1:]:
            self.find(*args[1:])

        return self

    def Find(self, *args):
        self.elems = self.elem = self.WD
        self.find(*args)
        return self

    def __find_one(self, *args: tuple):
        if not self.elem:
            self.assertion(f"Previous element = {self.elem}. Cant to find next {args} element")
            return
            # trying to find element
        try:
            elems = self.elem.find_elements(*args[:2])
        except NoSuchElementException:
            self.assertion(f"Element(s) not found: {args}")
            return
            # Check if list of number of element present
        if len(args) == 3 and isinstance(args[2], list) and all(isinstance(item, int) for item in args[2]):
            try:
                new_elems = [elems[i] for i in args[2]]
                elems = new_elems
            except IndexError:
                # self.assertion(f"Indexes of Elements incorrect: {args[2]}")
                pass
        self.elems = elems
        if self.elems:
            self.elem = self.elems[0]
            # print("elems:", self.elems)
            # print("elem", self.elem)
            return

        self.elem = None
        self.assertion(f"Element(s) not found: {args}, elems: {self.elems}, elem: {self.elem}")
        return

    def __get_tuple_depth(self, t):
        if isinstance(t, tuple):
            return 1 + max(self.__get_tuple_depth(i) for i in t)
        else:
            return 0

    def __args_normalizer(self, *args):
        # print("deep", self.__get_tuple_depth(args))
        # print("Start args", args)
        for i in range(self.__get_tuple_depth(args) - 2):
            args = sum(args, ())
        # print("Normaliser:", args)
        return args

    def find(self, *args):
        args = self.__args_normalizer(args)
        for by in args:
            self.__find_one(*by)

        return self

    def __checker(self, got, expect, message='') -> bool:

        if got == expect:
            self.print("Checked:", message, "... OK")
            return True

        self.assertion(f"!!! Wrong {message}")
        print("Got:", got)
        print("Expected:", expect)
        return False

    def title(self, title=''):
        if title:
            return self.__checker(self.WD.title, title, f"Title at: {self.WD.current_url}")

        return self.WD.title

    def current_url(self, url=''):
        if url:
            return self.__checker(self.WD.current_url, url, "Current_URL ")
        return self.WD.current_url

    def text(self, text=''):
        if text:
            return self.__checker(self.elem.text, text, f"Text at elements: {self.elem}")

        return self.elem.text

    def check_elem(self, message, *args):
        self.check_elem_in(message, self.WD, *args)

    def check_elem_in(self, message, elem, *args):
        if self.find_in(elem, *args):
            self.print(message, ": Element found:", args)
        else:
            self.print(message, "!!! Element NOT found:", args)

    def attr(self, attr, value=None):

        real_value = self.elem.get_attribute(attr)
        if real_value is None:
            print("!!! Attribute :", attr, "NOT found")
            self.assertion('Attribute not found')
            return None

        if value is None:
            return real_value

        return self.__checker(real_value, value, f"Attribute: {attr} with value: {value} for elements: {self.elem}")

    def Tag(self, tag_name):
        self.elems = self.elem = self.WD
        self.tag(tag_name)
        return self

    def tag(self, tag_name):
        elems = self.elem.find_elements(TAG, tag_name)
        if not elems:
            message = f"Elements not found by TAG NAME: {tag_name}"
            print("!!!", message)
            self.assertion(message)
            elems = []
        self.elems = elems
        self.elem = self.elems[0] if self.elems else None
        return self

    def contains(self, text):
        elems = []
        for elem in self.elems:
            if elem.text != text:
                continue
            elems.append(elem)

        # print("elems:", elems)
        self.elems = elems
        self.elem = self.elems[0] if self.elems else None

        # print("elem:", self.elem)
        # print("Filtering by text:", text)
        # return an instance of the same class
        return self

    def save_cookies_to_file(self, file_name):
        if self.wd_name in COOKIES:
            self.print("Cookies found")
            return
        COOKIES[self.wd_name] = self.WD.get_cookies()
        with open(file_name, 'a') as f:
            f.write(f'COOKIES = {COOKIES}\n')
            self.print("Cookies saved")


if __name__ == '__main__':
    time.sleep(15)
