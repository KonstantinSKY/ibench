import unittest
from login import Login


class Chrome_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Login("Chrome")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class Firefox_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Login("Firefox")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None


class Edge_Login(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = Login("Edge")

    def test_login(self):
        self.cls.login()

    def tearDown(self) -> None:
        self.cls.WD.close()
        self.cls = None
