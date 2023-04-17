from selen import Selen
from selen import TAG, CLASS, XPATH, NAME
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
    l_check_button = (CLASS, 'FrontPage_btnWrapper__2Q75S')
    l_btn = (TAG, "a")

    def __init__(self, wd="Chrome"):
        super().__init__(wd)
        self.url = "https://ibench.net/"
        self.assertions = False
        self.print_ok = True
        print()

    def main_page(self):
        self.WD.get(self.url)
        # self.Wait(self.l_h1).text('Looking for a developers, UX/UI designer, QA or DevOps...or development agency?')
        self.Tag('h1').text('Looking for a developers, UX/UI designer, QA or DevOps...or development agency?')
        self.title("iBench - real-time developers Hiring")
        self.curr_url("https://ibench.net/")
        print(self.Get_links(extract=True))
        self.check_links_a()
        sleep(5)

        # self.check_text("Looking for a developers, UX/UI designer, QA or DevOps...or development agency?", self.l_h1)
        # print(self.Tag("a").text1("Log in").elem)
        # self.Find(self.l_fp_registration)
        # self.Find(CLASS, 'FrontPage_btnWrapper__2Q75S')
        # self.Find(CLASS, 'FrontPage_btnWrapper__2Q75S', [0])
        # self.Find(self.l_login_btn)
        # self.Find(self.l_login_fields)
        # # self.Find(self.l_check_button, self.l_btn_wrap)

    def login(self):
        lc_fields = ((CLASS, "Login_form__2mvFD"), (TAG, "input"))
        lc_submit_button = ((CLASS, "Login_submit_wrapper__2-PYe"), (TAG, "button"))
        lc_validation = ((CLASS, "Login_form__2mvFD"), (CLASS, "form_group"))
        l_valid = (CLASS, "FrontPage_registrationLinks__2DkiO")

        self.main_page()
        # self.Find(self.l_login_btn).click()
        self.Tag('a').contains("Log in").click()

        self.Wait(self.l_h2).text("Log in")
        self.curr_url("https://ibench.net/login").title("Log in | iBench - real-time developers Hiring")

        # self.Find(NAME, "email").type(EMAIL).sleep(0.2).attr('value', EMAIL).parent(2).tag("span").attr('class', 'validation_status_ok')
        self.Find(NAME, "email").type(EMAIL).sleep(0.2).attr('value', EMAIL).parent(2).tag("span")
        self.attr('class', 'validation_status_ok')

        # print(self.elem.get_property('attributes')[0])
        print(self.Find(NAME, "email").all_attrs())
        print("CDC", self.Tag("form").count().tag("input").count().contains({'label': 'email', 'value': 'sky012877@gmail.com'}).elems)

        # self.Find(NAME, "email").parent(2).find(TAG, 'span').attr('class', 'validation_status_ok')
        # validations = self.finds(*lc_validation)

        # print("validations", validations)
        #
        # self.text_to_in(EMAIL, fields[0])
        # self.check_elem_in("Green checkmark at email", validations[0], l_valid)
        # self.check_attr_in("value", EMAIL, fields[0])
        #
        # self.text_to_in(PASSW, fields[1])
        # self.check_elem_in("Green checkmark at password", validations[1], l_valid)
        # self.click_to(*lc_submit_button)
        #
        # self.check_wait_text("Daily updates", self.l_h1)
        # self.check_url("https://ibench.net/stats")
        # self.check_title("Daily updates | iBench - real-time developers Hiring")
        # sleep(5)

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
