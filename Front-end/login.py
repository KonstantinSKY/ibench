from selen import Selen
from time import sleep
from security import EMAIL, PASSW


class Login(Selen):

    # locators
    l_login_btn = ("class name", "Navigation_login__JL_4K")
    l_login_field = ("xpath", "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]/form[1]/div[1]/div[1]/input[1]")
    l_password_field = ('xpath', "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]/form[1]/div[2]/div[1]/input[1]")
    l_login_btn_wrapper = ("class name", "Login_submit_wrapper__2-PYe")
    l_login_submit_btn = ("tag name", "button")

    # l_pag_href = ("tag name", "a")
    # l_tbody = ("tag name", "tbody")
    # l_tr = ("tag name", "tr")

    def __init__(self):
        super().__init__()
        self.url = "https://ibench.net/"

        # locators
        #l_login_btn = ("class", "Navigation_login__JL_4K")

        # l_pag_href = ("tag name", "a")
        # l_tbody = ("tag name", "tbody")
        # l_tr = ("tag name", "tr")


    def main(self):
        self.WD.get(self.url)
        self.wait_click_to(self.l_login_btn)
        sleep(1)
        self.wait_text_to(EMAIL, self.l_login_field)
        self.text_to(PASSW, self.l_password_field)
        self.click_login_btn()
        sleep(100)


if __name__ == "__main__":
    Login().main()
