from selen import Selen
from selen import TAG, CLASS, XPATH
from time import sleep
from security import EMAIL, PASSW


class iBench(Selen):
    # locators
    l_h1 = (TAG, "h1")
    l_h2 = (TAG, "h2")
    l_login_btn = (CLASS, "Navigation_login__JL_4K")
    l_login_fields = ((CLASS, "Login_form__2mvFD"), (TAG, "input"))

    l_fp_registration = (CLASS, "FrontPage_registrationLinks__2DkiO")
    l_btn_wrap = (CLASS, "FrontPage_btnWrapper__2Q75S")
    l_btn = (TAG, "a")

    def __init__(self, wd="Chrome"):
        super().__init__(wd)
        self.url = "https://ibench.net/"
        self.assertions = False
        self.print_ok = True
        print()

    def main_page(self):
        self.WD.get(self.url)
        self.check_title("iBench - real-time developers Hiring")
        self.check_url("https://ibench.net/")
        self.check_text("Looking for a developers, UX/UI designer, QA or DevOps...or development agency?", self.l_h1)

    def login(self):
        lc_fields = ((CLASS, "Login_form__2mvFD"), (TAG, "input"))
        lc_submit_button = ((CLASS, "Login_submit_wrapper__2-PYe"), (TAG, "button"))
        lc_validation = ((CLASS, "Login_form__2mvFD"), (CLASS, "form_group"))
        l_valid = (CLASS, "validation_status_ok")

        self.main_page()
        self.wait_click_to(self.l_login_btn)
        self.check_wait_text("Log in", self.l_h2)
        self.check_url("https://ibench.net/login")
        self.check_title("Log in | iBench - real-time developers Hiring")
        fields = self.finds(*lc_fields)
        validations = self.finds(*lc_validation)
        print("validations", validations)

        self.text_to_in(EMAIL, fields[0])
        self.check_elem_in("Green checkmark at email", validations[0], l_valid)
        self.check_attr_in("value", EMAIL, fields[0])

        self.text_to_in(PASSW, fields[1])
        self.check_elem_in("Green checkmark at password", validations[1], l_valid)
        self.click_to(*lc_submit_button)

        self.check_wait_text("Daily updates", self.l_h1)
        self.check_url("https://ibench.net/stats")
        self.check_title("Daily updates | iBench - real-time developers Hiring")
        sleep(5)

    def login_cookies(self):
        self.add_cookies()
        self.WD.get(self.url)
        sleep(20)
        # self.main_page()

    def registration(self):
        pass

    def recovery_password(self):
        pass

    def main(self):
        self.WD.close()


if __name__ == "__main__":
    iBench().login()
    sleep(10)
