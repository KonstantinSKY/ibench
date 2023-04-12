import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class Selen:

    def __init__(self, wd="Chrome", headless=False):
        
        if wd == "Chrome":
            opts = webdriver.ChromeOptions()
            opts.add_argument('--disable-blink-features=AutomationControlled')
            if headless:
                opts.add_argument('headless')
            opts.add_argument('window-size=1600x2600')
            self.WD = webdriver.Chrome(options=opts,  service=ChromeService(ChromeDriverManager().install()))

        self.WD.maximize_window()
        self.WD.act_chain = ActionChains(self)
    #
    # @staticmethod
    # def normalize_link(link: str):
    #     return link.strip().replace(" ", "%20")
    #
    # def get(self, link):
    #     self.drv.get(self.url + link)
    #
    # def set_elem_attrs(self):
    #     setattr(self.elem, "find", self.elem.find_element)
    #     setattr(self.elem, "finds", self.elem.find_elements)

    def wait_find(self, by: tuple):
        try:
            self.elem = WebDriverWait(self, 10).until(EC.presence_of_element_located(by))
        finally:
            return self.elem

    def get_elem(self, find_func):
        self.get(self.url + self.link)
        self.elem = find_func()
        return self.elem

    def get_elems(self, find_func):
        self.elems = []
        for link in self.links:
            # self.get(self.url + link)
            self.elems.extend(find_func())
            elems = find_func()
            print(len(elems))
            time.sleep(1)
            break
            # print(self.elems)
        return self.elems
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
    # S = Dappradar()
    # print(sorted(S.__dict__))
    # print(sorted(S.__dir__()))
    # S.get("https://dappradar.com/rankings/category/games")
    Dappradar().main()
    time.sleep(5)
    Dappradar().get("https://dappradar.com/multichain/games/alien-worlds")
    time.sleep(15)
