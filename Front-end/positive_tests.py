import unittest
from ibench import iBench as Cls


class Chrome_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Cls("Chrome")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class Firefox_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Cls("Firefox")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class Edge_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Cls("Edge")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class Opera_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Cls("Opera")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None
