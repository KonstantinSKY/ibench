# Import class Selen and simple Locator names and variables
from selen import *

from time import sleep
# file
from security import EMAIL, PASSW


# Class of project
class iBench(Selen):

    def __init__(se, wd="Chrome"):
        super().__init__(wd)
        # Web-site and tests environment settings
        se.url = "https://ibench.net/"
        se.ok_assert = False
        se.ok_print = True

    # locators
    l_login_btn = (CLASS, "Navigation_login__JL_4K")
    l_login_fields = ((CLASS, "Login_form__2mvFD"), (TAG, "input"))

    l_fp_registration = (CLASS, "FrontPage_registrationLinks__2DkiO")
    l_btn_wrap = (CLASS, "FrontPage_btnWrapper__2Q75S")
    l_check_button = (CLASS, 'FrontPage_btnWrapper__2Q75S')
    l_btn = (TAG, "a")

    def main_page(se):
        se.WD.get(se.url)  # Get page from WD
        # New Wait method

        # Wait element and check inner text
        se.Wait(l_h1).text('Looking for a developers, UX/UI designer, QA or DevOps...or development agency?')

        se.Tag("head").out("head:")
        se.Cls('FrontPage_clientImage__3KW8O').text().out("Image Page")

        se.Tag('h1').text().out("Text of element:")
        se.Tag('h1').xpath_query().out()

        se.title('iBench - real-time developers Hiring')  # Check title
        se.title().out("Page title:")  # Output of page title

        se.Cls('FrontPage_btnWrapper__2Q75S').out("Wrapper element:")

        se.curr_url().out("URL:")  # Output URL
        se.curr_url("https://ibench.net/")  # Check url
<<<<<<< HEAD
        # se.check_links(asynchron=True)
=======
        # se.check_links(asynchron=False).stat.out("Link Statistic")
>>>>>>> cce5c6de178f0b4265858631baa65e2e90eed5fd

        # Checking images on the page
        # se.Img(check=True).sleep(10)  # Check all Images
        se.Img(check=True).stat.out()  # Check all Images

    def login(se):
        lc_submit_button = ((CLASS, "Login_submit_wrapper__2-PYe"), (TAG, "button"))

        se.main_page()
        se.Contains("Log in").click()
<<<<<<< HEAD
        #se.Wait(l_h2).text("Log in")
        #se.Img(check=True)
=======
        #se.Wait(l_h2).text("Login").click()

>>>>>>> cce5c6de178f0b4265858631baa65e2e90eed5fd
        se.curr_url("https://ibench.net/login").title("Log in | iBench - real-time developers Hiring")

        se.Find(NAME, "email").type(EMAIL).sleep(0.2).attr('value', EMAIL).out()
        se.parent(2).tag("span").attr('class', 'validation_status_ok')
        se.Find(NAME, "email").xpath_query().out("XPath")
        se.Find(NAME, "password").type(PASSW).sleep(0.2).attr('value', PASSW)
        se.parent(2).tag("span").attr('class', 'validation_status_ok')

        se.Find(*lc_submit_button).click()
        # se.sleep(10)
        se.Wait(l_h1).text("Daily updates")
        se.curr_url("https://ibench.net/stats")
        se.title("Daily updates | iBench - real-time developers Hiring")
        sleep(10)



    def login_cookies(self):
        self.add_cookies()
        self.WD.get(self.url)
        sleep(20)
        # self.main_page()

    def registration(self):
        pass

    def recovery_password(self):
        pass

    def main(se):
        pass


if __name__ == "__main__":
    iBench().login()
    sleep(10)
