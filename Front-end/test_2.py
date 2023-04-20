import unittest
from ibench import iBench as Cls


class ChromeLoginTest(unittest.TestCase):
    browser_name = "Chrome"

    def setUp(self) -> None:
        self.cls = Cls(self.browser_name)

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class FirefoxLoginTest(ChromeLoginTest):
    browser_name = "Firefox"


class EdgeLoginTest(ChromeLoginTest):
    browser_name = "Edge"


class OperaLoginTest(ChromeLoginTest):
    browser_name = "Opera"


