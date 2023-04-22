import json
import time
from random import uniform
from collections import Counter
import aiohttp
import asyncio
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as OperaService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

from security import COOKIES
from collections import Counter

# from webdriver_manager.safari import SafariDriverManager

ID = "id"
TAG = "tag name"
XPATH = "xpath"
CLASS = "class name"
NAME = "name"
LINK = "link text"
PART_LINK = "partial link text"
CSS = "css selector"
# main tag names locators
l_h1 = (TAG, "h1")
l_h2 = (TAG, "h2")
l_a = (TAG, "a")
l_input = (TAG, "input")


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

        elif wd == "Opera":
            opts = webdriver.ChromeOptions()
            # opts.binary_location = "/usr/bin/opera"
            opts.add_experimental_option('w3c', True)
            self.WD = webdriver.Chrome(service=OperaService(OperaDriverManager().install()), options=opts)

        else:
            print('!!! WebDriver for: ', wd, " does NOT Exits in the system.")
            exit()

        self.elems = []
        self.elem = WebElement
        self.links = []
        self.images = {}
        self.wd_name = wd
        self.out_str = ''
        self.WD.maximize_window()
        self.AC = ActionChains(self.WD)
        self.WDW = WebDriverWait(self.WD, 10)
        self.url = ""
        self.ok_assert = True
        self.ok_print = True
        self.stat = {}
        self.IS = None

    class Out_str(str):
        def out(self, message=''):
            print(message, self)

    class Out_dict(dict):
        def out(self, message=''):
            print(message)
            print(json.dumps(self, indent=4))

    def __start(self):
        self.elems = self.elem = self.WD
        self.IS = None

    # Service function Fill elems variables (self.elem, self.elems after operation with WebDriver
    def __fill_elems(self, data):
        if isinstance(data, list):
            self.elems = data
            self.elem = self.elems[0] if self.elems else None
        else:
            self.elem = data
            self.elems = [self.elem]

    # Service get depth od tuples in tuples
    def __get_tuple_depth(self, t):
        if isinstance(t, tuple):
            return 1 + max(self.__get_tuple_depth(i) for i in t)
        else:
            return 0

    # Service method to normalize any arguments to tuple of tuples standard
    def __args_normalizer(self, *args):
        for i in range(self.__get_tuple_depth(args) - 2):
            args = sum(args, ())
        return args

    # Print text to STDOUT if it set
    def print(self, *args, **kwargs):
        if self.ok_print:
            print(*args, **kwargs)

    # def out(self, message=''):
    #     print(message, self.output)

    # Run assertion if it set
    def assertion(self, message=''):
        print("!!!", message)
        if self.ok_assert:
            assert False, message

    # Delay chain function. Possible to set random delay between two parameters.
    def sleep(self, seconds, finish=None):
        if finish is None:
            self.print("Sleeping for:", seconds, "seconds")
            time.sleep(seconds)
            return self

        delay = uniform(seconds, finish)
        self.print("Sleeping for:", delay, "seconds")
        time.sleep(uniform(seconds, finish))
        return self

    # --------   Functions of findings, selecting elements -----------
    # The Wait chain function finds and waits for appear element and save elems variables
    def Wait(self, *args):
        self.__start()
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

    # Find element(s) by arguments for all page elements and from WebDriver directly
    def Find(self, *args):
        self.__start()
        self.find(*args)
        return self

    # Find element(s) inside other element self.elem by arguments
    def find(self, *args):
        self.IS = None
        args = self.__args_normalizer(args)
        print(args)
        for by in args:
            self.__find_one(*by)

        return self

    # Service function for the element finding
    def __find_one(self, *args: tuple):
        if not self.elem:
            self.assertion(f"Previous element = {self.elem}. Cant to find next {args} element")
            return
            # trying to find element
        print("args", args)
        try:
            elems = self.elem.find_elements(*args[:2])
        except NoSuchElementException:
            self.assertion(f"Element(s) not found: {args}")
            return

        if len(args) > 2:
            new_elems = []
            for arg in args[2:]:
                if isinstance(arg, int) and 0 <= arg < len(elems):
                    new_elems.append(elems[arg])
                else:
                    print("Wrong index of elements", arg, "maximum is", len(elems))
            elems = new_elems

        self.elems = elems
        if self.elems:
            self.elem = self.elems[0]
            return

        self.elem = None
        self.assertion(f"Element(s) not found: {args}, elems: {self.elems}, elem: {self.elem}")
        return

    # Find element by tag name,  chain function for all page elements and from WebDriver directly
    def Tag(self, tag_name: str, *idx):
        self.__start()
        self.tag(tag_name, *idx)
        return self

    # Find element by tag name inside other elements in self.elems
    def tag(self, tag_name: str, *idx):
        self.find((TAG, tag_name, *idx))
        return self

    # Find element by Class name,  chain function for all page elements and from WebDriver directly
    def Cls(self, class_name: str, *idx):
        self.__start()
        self.cls(class_name, *idx)
        return self

    # Find element by tag name inside other elements in self.elems
    def cls(self, class_name: str, *idx):
        self.find((CLASS, class_name, *idx))
        return self

        # Find element by Class name,  chain function for all page elements and from WebDriver directly

    def Xpath(self, query: str, *idx):
        self.__start()
        self.cls(query, *idx)
        return self

        # Find element by tag name inside other elements in self.elems

    def xpath(self, class_name: str, *idx):
        self.find((CLASS, class_name, *idx))
        return self

    def Id(self, id_name: str, *idx):
        self.Find(id_name, *idx)

    # Get all image from all page from WebDriver object and optional checking and install
    def Img(self, *idx, check=False):
        self.__start()
        self.img(*idx, check=check)
        return self

    # Get all image from element self.elem and optional checking and extract
    def img(self, *idx, check=False):
        self.tag('img', *idx)
        self.print("Found images:", len(self.elems))
        self.images = self.Out_dict({})
        for image in self.elems:
            xpath = self.xpath_query(image)
            src = image.get_attribute("src")
            alt = image.get_attribute("alt")
            visible = image.is_displayed()
            self.images[xpath] = {'source': src, 'alt': alt, 'visible': visible}
            self.print(f"Image: xpath: {xpath}, source: {src}, alt = {alt}, visible: {visible}")
            # self.WD.execute_script("arguments[0].style.display = 'block';", image)
            if not check:
                continue
            ok = True
            if not src:
                ok = False
                print(f"!!! Image without source, xpath: {xpath}")
            if not visible:
                ok = False
                print(f"!!! Invisible Image, xpath: {xpath}")
            if not alt:
                ok = False
                print(f"!!! Image without ALT attribute, xpath: {xpath}")
            # checked if loaded
            complete = self.WD.execute_script("return arguments[0].complete", image)
            n_width = self.WD.execute_script("return arguments[0].naturalWidth > 0", image)
            if not complete or not n_width:
                ok = False
                print(f"!!! Image not loaded, xpath:{xpath}. Arguments: Complete={complete}, naturalWidth={n_width}")
                self.images[xpath]['loaded'] = False
            else:
                self.images[xpath]['loaded'] = True
            if ok:
                print("Checked  ... OK")
        self.print("Got images:", len(self.images))
        return self

    # Selecting Element filter by contain data(text and attributes) from all elements on Page from WD
    def Contains(self, data, *idxs):
        self.__start()
        self.__fill_elems(self.WD.find_elements(XPATH, "//*"))
        self.print("Count", len(self.elems))

        self.contains(data, *idxs)

    # Selecting Element filter by contain data(text and attributes) from other element self.elem
    def contains(self, data, *idxs):
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

        if len(idxs) > 0:
            new_elems = []
            for idx in idxs[2:]:
                if isinstance(idx, int) and 0 <= idx < len(elems):
                    new_elems.append(elems[idx])
                else:
                    print("Wrong index of elements", idx, "maximum is", len(elems))
            elems = new_elems

        self.__fill_elems(elems)
        return self

    # Select parent element of self.elem, can use number of parent level, default = 1
    def parent(self, levels=1):
        self.IS = None
        for i in range(levels):
            try:
                self.__fill_elems(self.find(XPATH, '..'))
            except NoSuchElementException:
                self.assertion(f"Parent Element at level {i} not found")
        return self

    # -------------- Functions for actions with found element(s) ----------------
    # Click chain function have 2 modes simple and with action chains with pause.
    def click(self, action=False, pause=0):
        if action:
            self.__action_click(pause=pause)
        else:
            self.elem.click()
        self.print("Clicked element:", self.elem)
        return self

    # Context Click chain function with pause.
    def context_click(self, pause=0):
        self.__action_click(mode='context', pause=pause)
        self.print("Context Clicked element:", self.elem)
        return self

    # Double Click with action chains and pause.
    def double_click(self, pause=0):
        self.__action_click(mode='double', pause=pause)
        self.print("Double Clicked element:", self.elem)
        return self

    # Service functions for any clicks
    def __action_click(self, mode='', pause=0):
        self.AC.move_to_element(self.elem)
        if pause > 0:
            self.print("Pause before click, seconds:", pause)
            self.AC.pause(pause)
        under = '_' if mode else ''
        eval(f"self.AC.{mode}{under}click()")
        self.AC.perform()

    # Display hidden and invisible element
    def display(self, elem=None):
        elem = self.elem if elem is None else elem

        if elem.is_displayed():
            self.print("Element VISIBILITY already is ON, xpath:", self.xpath_query(elem))
        else:
            self.WD.execute_script("arguments[0].style.display = 'block';", elem)
            print("Element VISIBILITY switched ON, xpath:", self.xpath_query(elem))
        return self

    # Text of element (self.elem) It has 2 mode text return or check if the text presents
    def title(self, title=''):
        self.out_str = self.Out_str(self.WD.title)
        if title:
            self.IS = self.__checker(self.WD.title, title, f"Title at: {self.WD.current_url}")
            return self
        return self.out_str

    # Current URL of current page
    def curr_url(self, url=''):
        self.out_str = self.Out_str(self.WD.current_url)
        if url:
            self.__checker(self.WD.current_url, url, "Current_URL ")
            return self
        return self.out_str

    # Text of element (self.elem) It has 2 mode text return or check if the text presents
    def text(self, text=None):
        self.out_str = self.Out_str(self.elem.text)
        if text is None:
            return self.out_str
        self.__checker(self.elem.text, text, f"Text {self.elem.text} at element: {self.xpath_query()}")
        return self

    # Type text in the element (self.elem)
    def type(self, text):
        self.out_str = self.Out_str(self.elem.text)
        self.elem.click()
        self.elem.clear()
        self.elem.send_keys(text)
        return self

    # Print count of selected elements of check if the count of element == asked counts and returns
    def count(self, num=None):
        count = len(self.elems)
        self.out_str = self.Out_str(str(count))
        if num is None:
            self.print("Count of Elements:", count)
            return count
        self.__checker(count, num, f"Count of  elements: {self.elem}")
        return self

    # Return absolute xpath of Element or None if not found
    def xpath_query(self, elem=None) -> str or None:
        elem = self.elem if elem is None else elem
        xpath = self.WD.execute_script("""
                var xpath = "";
                var containerElem = document.documentElement;
                var elem = arguments[0];

                while (elem !== containerElem) {
                    var index = 0;
                    var sibling = elem.previousSibling;

                    while (sibling) {
                        if (sibling.nodeType === Node.ELEMENT_NODE && 
                            sibling.nodeName.toLowerCase() === elem.nodeName.toLowerCase()) {
                            index++;
                        }
                        sibling = sibling.previousSibling;
                    }
                    xpath = "/" + elem.nodeName.toLowerCase() + "[" + (index + 1) + "]" + xpath;
                    elem = elem.parentNode;
                }
                return "/" + containerElem.nodeName.toLowerCase() + xpath;
        """, elem)  # Checking for correct XPATH
        try:
            self.WD.find_element(XPATH, xpath)
            return xpath
        except NoSuchElementException:
            self.assertion(f"!!! Found Incorrect abs XPATH, Got {xpath} but Can not to find Element by it")
            return None

    # Check attribute of self.elem, if exists,  for value, if value is None returns value
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

    # return all attributes of element
    def all_attrs(self, elem=None) -> dict:
        elem = self.elem if elem is None else elem
        attrs = self.WD.execute_script("""
             var items = {}; 
             for (index = 0; index < arguments[0].attributes.length; ++index) { 
                 items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
             }; 
             return items;
             """, elem)
        return attrs

    # -------------- Functions for check any data with found element(s) ----------------
    # Service method for compare two parameter and retur
    def __checker(self, got, expect, message='') -> bool:
        if got == expect:
            self.print("Checked:", message, "... OK")
            # self.output = self.Output("True")
            return True

        self.assertion(f"!!! Wrong {message}")
        print("Got:", got)
        print("Expected:", expect)
        # self.output = self.Output("False")
        return False


    # --------- Links methods ------------------------------
    # Get all links from all page with WebDriver
    def Get_links(self, extract=False, check=False, asynchron=True):
        self.elems = self.elem = self.WD
        self.get_links(extract, check, asynchron=asynchron)
        return self.links if extract else self

    # Get all links from self.elem  page with WebDriver
    def get_links(self, extract=False, check=False, asynchron=True):
        self.links = []
        self.tag('a')
        for link in self.elems:
            if link.get_attribute('href'):
                self.links.append(link.get_attribute('href'))
            else:
                print(f"!!! Incorrect link: No attribute 'href', xpath: {self.xpath_query(link)}")
        self.links = list(set([link for link in self.links if not link.startswith("mailto:")]))
        self.print("Got ", len(self.links), "links, Saved to self.links variable")
        if check:
            self.check_links(asynchron=asynchron)
        return self.links if extract else self

    # Check links for response 200, selecting of mode sync or async
    def check_links(self, asynchron=True):
        if asynchron:
            self.print('Async link checking...')
            asyncio.run(self.__check_links_async())
        else:
            self.print('Sync links checking...')
            self.__check_links_sync()

    # Links response sync checking
    def __check_links_sync(self):
        self.stat = {}
        for link in self.links:
            try:
                response = requests.get(link)
                self.__response_stat(link, response.status_code)
            except:
                print("Unable to reach:", link)
        self.__summary_stat()

    # Links response async checking
    async def __check_links_async(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for link in self.links:
                task = asyncio.create_task(self.__check_link_async(link, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            self.stat = {}
            for response in responses:
                self.__response_stat(response.url, response.status)
            self.__summary_stat()

    async def __check_link_async(self, link, session):
        async with session.get(link) as response:
            return response

    def __summary_stat(self):
        counts = Counter(self.stat.values())
        self.print("Checked:", len(self.links), ", Status 200 OK is", counts[200])
        self.print("All statuses:", self.stat)

    def __response_stat(self, url, status):
        self.stat[url] = status
        print(len(self.stat))
        if status == 200:
            self.print(url, "OK")
        elif status == 404:
            self.assertion(f"Broken link found: {url}")
        else:
            print(f"Unable to reach: {url}")

    # --------- Image Methods ---------------------------

    # -----------Methods for cookies  -----------------
    def add_cookies(self):
        for cookie in COOKIES[self.wd_name]:
            self.WD.execute_cdp_cmd('Network.setCookie', cookie)
            # self.WD.add_cookie(cookie)

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
