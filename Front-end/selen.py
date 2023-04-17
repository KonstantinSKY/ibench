import time
from random import uniform
import requests, asyncio, aiohttp

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
        self.links = []
        self.wd_name = wd
        self.WD.maximize_window()
        self.WD.act_chain = ActionChains(self)
        self.WDW = WebDriverWait(self.WD, 10)
        self.url = ""
        self.assert_ok = True
        self.print_ok = True
        self.statuses = {}

    def __fill_elems(self, data):
        if isinstance(data, list):
            self.elems = data
            self.elem = self.elems[0] if self.elems else None
        else:
            self.elem = data
            self.elems = [self.elem]

    def add_cookies(self):
        for cookie in COOKIES[self.wd_name]:
            self.WD.execute_cdp_cmd('Network.setCookie', cookie)
            # self.WD.add_cookie(cookie)

    def print(self, *args, **kwargs):
        if self.print_ok:
            print(*args, **kwargs)

    def sleep(self, seconds, finish=None):
        if finish is None:
            self.print("Sleeping for:", seconds, "seconds")
            time.sleep(seconds)
            return self

        delay = uniform(seconds, finish)
        self.print("Sleeping for:", delay, "seconds")
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
        # self.print("Waiting and Looking for :", args)
        try:
            elem = self.WDW.until(EC.presence_of_element_located(args[0]))
        except NoSuchElementException:
            self.assertion(f"Element not found: {args[0]}")
            return
        except TimeoutException:
            print("Command timed out!")
            self.assertion(f"Element not found: {args[0]}")
            return

        self.print("Wait Element found", args[0], " ... OK")
        self.__fill_elems(elem)

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
        for i in range(self.__get_tuple_depth(args) - 2):
            args = sum(args, ())
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

    def is_title(self, title: str) -> bool:
        return title == self.WD.title

    def title(self, title=''):
        if title:
            self.__checker(self.WD.title, title, f"Title at: {self.WD.current_url}")
            return self
        return self.WD.title

    def is_curr_url(self, url):
        return url == self.WD.current_url

    def curr_url(self, url=''):
        if url:
            self.__checker(self.WD.current_url, url, "Current_URL ")
            return self
        return self.WD.current_url

    def is_text(self, text):
        return text == self.elem.text

    def text(self, text=None):
        if text is None:
            return self.elem.text
        self.__checker(self.elem.text, text, f"Text at elements: {self.elem}")
        return self

    def parent(self, levels=1):
        for i in range(levels):
            try:
                self.__fill_elems(self.elem.find_element(By.XPATH, '..'))
            except NoSuchElementException:
                self.assertion(f"Parent Element at level {i} not found")
        return self

    def type(self, text=None):
        self.elem.click()
        self.elem.clear()
        self.elem.send_keys(text)
        return self

    def is_attr(self, attr, value):
        return value == self.elem.get_attribute(attr)

    def attr(self, attr, value=None):
        real_value = self.elem.get_attribute(attr)

        if real_value is None:
            print("!!! Attribute :", attr, "NOT found")
            self.assertion('Attribute not found')
            return self

        if value is None:
            return real_value

        self.__checker(real_value, value, f"Attribute: {attr} with value: {value} for elements: {self.elem}")
        return self

    def all_attrs(self) -> dict:
        attrs = self.WD.execute_script("""
            var items = {}; 
            for (index = 0; index < arguments[0].attributes.length; ++index) { 
                items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
            }; 
            return items;
            """, self.elem)
        return attrs

    def Tag(self, tag_name: str):
        self.elems = self.elem = self.WD
        self.tag(tag_name)
        return self

    def tag(self, tag_name: str):

        elems = self.elem.find_elements(By.TAG_NAME, tag_name)
        if not elems:
            message = f"Elements not found by TAG NAME: {tag_name}"
            print("!!!", message)
            self.assertion(message)
            elems = []
        self.__fill_elems(elems)
        return self

    def count(self):
        self.print("Count of Elements:", len(self.elems))
        return self

    # Links getting
    def Get_links(self, extract=False, check=False, asynchron=True):
        self.elems = self.elem = self.WD
        self.get_links(extract, check, asynchron=asynchron)
        return self.links if extract else self

    def get_links(self, extract=False, check=False, asynchron=True):
        self.tag('a')
        self.links = list(set([elem.get_attribute('href') for elem in self.elems]))
        self.links = [link for link in self.links if not link.startswith("mailto:")]
        self.print("Got ", len(self.links), "links, Saved to self.links variable")
        if check:
            self.check_links(asynchron=asynchron)
        return self.links if extract else self

    def check_links(self, asynchron=True):
        if asynchron:
            self.print('Async link checking...')
            asyncio.run(self.__check_links_async())
        else:
            self.print('Sync links checking...')
            self.__check_links_sync()

    # Links checking
    def __check_links_sync(self):
        for link in self.links:
            try:
                response = requests.get(link)
                self.__response_stat(link,response.status_code)
            except:
                print("Unable to reach:", link)
        self.__summary_stat()

    async def __check_links_async(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for link in self.links:
                task = asyncio.create_task(self.__check_link_async(link, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            self.statuses = {}
            for response in responses:
                self.__response_stat(response.url, response.status)
            self.__summary_stat()

    async def __check_link_async(self, link, session):
        async with session.get(link) as response:
            return response

    def __summary_stat(self):
        self.print("Checked:", len(self.links), ", Status 200 OK is", self.statuses[200])
        self.print("All statuses:", self.statuses)

    def __response_stat(self, url, status):
        if status in self.statuses:
            self.statuses[status] += 1
        else:
            self.statuses[status] = 1

        if status == 200:
            self.print(url, "OK")
        elif status == 404:
            self.assertion(f"Broken link found: {url}")
        else:
            print(f"Unable to reach: {url}")

    # Element filter by contain data
    def Contains(self, data=None):
        self.__fill_elems(self.WD.find_elements(XPATH, "//*"))
        self.print("Count", len(self.elems))
        if data is None:
            return self

        self.contains(data)

    def contains(self, data):
        elems = []
        if isinstance(data, dict):
            for self.elem in self.elems:
                result = False
                print("elem", self.elem)
                for attr, value in data.items():
                    if not self.is_attr(attr, value):
                        result = False
                        print("attr", attr, "not found")
                        break
                    result = True
                    print("attr:", attr, value, "found")
                if not result:
                    continue
                elems.append(self.elem)

        if isinstance(data, str):
            for elem in self.elems:
                if elem.text != data:
                    continue
                elems.append(elem)

        self.__fill_elems(elems)

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
