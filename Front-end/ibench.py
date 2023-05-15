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

    def home(se):
        se.WD.get(se.url)  # Get page from WD
        # Wait element and check inner text
        se.Wait(l_h1).text('Looking for a developers, UX/UI designer, QA or DevOps...or development agency?')
        se.title('iBench - real-time developers Hiring')  # Check title
        se.curr_url("https://ibench.net/")  # Check url
        se.Img(check=True).stat.out()  # Check all Images
        # se.check_links(asynchron=True).sleep(0, 3)  # Check all Links

        # se.Tag("head").out("head:")
        # se.Cls('FrontPage_clientImage__3KW8O').text().out("Image Page")
        # se.Tag('h1').text().out("Text of element:")
        # se.Tag('h1').xpath_query().out()
        # se.title().out("Page title:")  # Output of page title
        # se.Cls('FrontPage_btnWrapper__2Q75S').out("Wrapper element:")
        # se.curr_url().out("URL:")  # Output URL
        # se.check_links(asynchron=False).stat.out("Link Statistic")
        # Checking images on the page
        # se.Img(check=True).sleep(10)  # Check all Images

    def login(se):
        lc_submit_button = ((CLASS, "Login_submit_wrapper__2-PYe"), (TAG, "button"))  # Submit button locator

        se.home()  # Start main page
        se.Contains("Log in").click().Wait(l_h2).text("Log in")  # Click to login and wait for new page header with tex
        se.curr_url("https://ibench.net/login").title("Log in | iBench - real-time developers Hiring")
        # se.Img(check=True).check_links()

        # Enter email and password with checking for update 'value' attribute and green checkmarks
        se.Find(NAME, "email").type(EMAIL).sleep(0.2).attr('value', EMAIL).out()
        se.parent(2).tag("span").attr('class', 'validation_status_ok')
        # se.Find(NAME, "email").xpath_query().out("XPath")
        se.Find(NAME, "password").type(PASSW).sleep(0.2).attr('value', PASSW)
        se.parent(2).tag("span").attr('class', 'validation_status_ok')

        # se.Find(*lc_submit_button).click().sleep(2)  #click submit button
        se.Tag('button').click().sleep(2, 4)

        se.Wait(l_h1).text("Daily updates")
        se.curr_url("https://ibench.net/stats").title("Daily updates | iBench - real-time developers Hiring")
        # se.Img(check=True).check_links()

        sleep(1)

        # se.Find(NAME, "email").xpath_query().out("XPath")
        # se.Wait(l_h2).text("Log in")
        # se.Img(check=True)
        # se.Wait(l_h2).text("Login").click()

    def about(se):
        se.Wait(l_h1).text(
            """iBench is an easy hiring way to find new highly-skilled Remote developers in 2-3 business days after your request.""")
        se.curr_url('https://ibench.net/about').title('About | iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def blog(se):
        se.Wait(CLASS, "breadcrumbs").Tag("span", 1).text("Blog")
        se.curr_url('https://ibench.net/blog/').title('iBench - iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def hire_remote_team(se):
        se.Wait(l_h1).text('Hire remote developers team')
        se.title().out("Title :")
        se.title("iBench - real-time developers Hiring")
        se.curr_url('https://ibench.net/team-search')  # .title('About | iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def support_slack(se):
        se.Wait(CLASS, 'c-link').img().attr("alt", "Slack")

    def privacy(se):
        se.Wait(l_h1).text('Privacy Notice')
        se.curr_url('https://ibench.net/privacy-policy').title('Privacy Notice | iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def cookie(se):
        se.Wait(l_h1).text('Cookie Policy')
        se.curr_url('https://ibench.net/cookie-policy').title('Cookie Policy | iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def terms(se):
        se.Wait(l_h1).text('Terms Of Use')
        se.curr_url('https://ibench.net/terms-of-use').title('Terms Of Use | iBench - real-time developers Hiring')
        se.Img(check=True).check_links()

    def nav_menu(se, locator):
        texts = [elem.text for elem in se.Wait(locator).elems]
        for text in texts:
            se.Find(locator).contains(text)
            func = text.lower().replace(" ", "_")
            print("Checking menu element... ", func)
            old_url = se.curr_url()
            se.click()
            eval(f"se.{func}()")
            if old_url != se.curr_url():
                se.WD.back()
            sleep(1)

    def head_nav_menu(se):
        se.WD.get(se.url)  # Get page from WD
        se.Wait(CLASS, 'Navigation_menu__Xg4DA').tag('a')
        se.nav_menu(((CLASS, 'Navigation_menu__Xg4DA'), (TAG, 'a')))

    def foot_nav_menu(se):
        se.WD.get(se.url)  # Get page from WD
        se.Wait(CLASS, "cookieinfo-close").click()
        se.nav_menu(((CLASS, 'Footer_menu__3wGBS'), (TAG, 'a')))

    def login_cookies(se):
        se.add_cookies()
        se.WD.get(se.url + 'stats')
        sleep(20)
        # self.main_page()

    def registration(se):
        se.get({
            "wait": (CLASS, "Navigation_btn__3RPM8"),
            "title": "iBench - real-time developers Hiring" 
        })

        # se.Wait(CLASS, "Navigation_btn__3RPM8").text("Register").out("Message: ")
        # se.title("iBench - real-time developers Hiring").curr_url("https://ibench.net/")
        # se.Cls("Navigation_auth_buttons__29gW3").out().contains("Register").out()
        # se.Find(NAME, "password_copy").type("AlexCool2604").attr("value", "AlexCool2604")
        se.Contains("Register").click()
        se.Wait(TAG, "h2").text("Create your iBench account")
        se.title("Registration | iBench - real-time developers Hiring").curr_url("https://ibench.net/registration")
        se.Find(NAME, "email").click(action=True).type("AlexCool2604").attr("value", "AlexCool2604")
        se.Tag("select").dropdown_select(34)
        sleep(30)
        # se.Find(NAME, 'terms_accepted').click(action=True, pause=3)
        # se.Contains({'name': 'terms_accepted'}).parent().out()#.display() #parent().click(action=True)
        # se.Contains({'name': 'terms_accepted'}).out()
        # se.Cls("FormControls_checkmark__Ze3F_").click()
        se.WD.find_element(By.CLASS_NAME, "FormControls_checkmark__Ze3F_")

        #
        # se.Find(NAME, "password").type("AlexCool2604").attr("value", "AlexCool2604")
        sleep(150)
        # se.Find(NAME, "password_copy").sleep(2).type("AlexCool2604").attr("value", "AlexCool2604")
        # # se.Img(check=True)
        # se.Xpath("/html/body[1]/div[2]/span[1]/img[1] ").display()
        # # se.Img(check=True)
        # # se.check_links()
        # se.Contains("Client").click()
        # se.Find(NAME, "email").type("sdfds@sdsdas.com").sleep(2).attr("value", "sdfds@sdsdas.com").parent(2)
        # se.tag("span").attr('class', 'validation_status_ok')
        # # se.Cls("validation_status_ok").attr("class", "validation_status_ok")
        #
        se.sleep(20)

    def recovery_password(se):
        # se.WD.get(se.url+"login")
        # se.get("recovery")
        se.get("recovery", {
            "wait": (TAG, "h1"),  # l_h1,
            "title": "iBench - real-time developers Hiring",
        })

        # se.check_page({
        #     "wait": l_h1,
        #     "title": "iBench - real-time developers Hiring",
        #     "url": se.url+"login"
        # })
        #

        #
        # })
        # se.Wait(l_h2).text('Log in')
        # se.Cls("Login_recovery_link__1asIj").sleep(1, 3).click()
        # se.Wait(l_h1).text("Recovery password")
        # se.title().out()
        # se.curr_url("https://ibench.net/krecovery").title("Recovery password | iBench - real-time developers Hiring")
        # se.Img(check=True)
        # se.check_links()
        # se.Contains({"name": "email", "type": "email"}).out()

        # se.Find(NAME, "email").type(EMAIL).sleep(0.2).attr('value', EMAIL)
        # se.Cls('validation_status_ok')
        # se.Contains("Submit").click()
        # se.print("python")

        # print("-"*100)

        sleep(10)

    def sell_lead(se):
        se.login()
        se.Cls("DashboardMenu_menuLink__JkSw7").contains("Sell leads").click()
        se.check_page({"wait": (TAG, "h1"),
                       "url": "https://ibench.net/sell-leads",
                       "title": "Developers | iBench - real-time developers Hiring"
                       })

        se.Find(CLASS, "SellLeadButton_sellLeadsButton__3c0L8").click('')
        se.check_page({"wait": (TAG, "form"),
                       "url": "https://ibench.net/add-lead",
                       "title": "Sell leads | iBench - real-time developers Hiring"
                       })

        se.Wait(NAME, "vetted").dropdown_select()
        se.Cls("LeadForm_leadType__XWd1z").tag("span").click(random=True)
        se.Cls("LeadForm_qualificationLevelType__3PXrP").tag("span").click(random=True)
        se.Find(NAME, "fixed_price").type("10000")
        se.Find(NAME, "lead_sales_comment").type("Test comments 1")
        se.Find(NAME, "country").dropdown_select()
        se.Tag("button").contains("Next").click()
        se.Wait(CLASS, "LeadForm_aboutProject__OxQEz").text("About Project")
        se.Find(NAME, "project_type_id").dropdown_select()
        se.Find(NAME, "project_name").type("Project1")
        se.Find(NAME, "project_description").type("Project descr")
        se.Find(NAME, "budget").type(23423)
        se.Find(CLASS, "ant-picker-input").tag("input").elem.send_keys("04/06/2023")
        se.Find(NAME, "description_link").type("ibench.us")
        se.Find(NAME, "additional_comment").type("additional comment")
        se.Find(CLASS, "LeadForm_submit__1Ax9Y").click()
        se.Wait(CLASS, "CongratsModal_modalHeader__yA0p6").text("Congrats!")
        se.Find(CLASS, "CongratsModal_gotItButton__tJFaf").click()

        se.check_page({"wait": (TAG, "h1"),
                       "url": "Marketplace / Leads | iBench - real-time developers Hiring",
                       "title": "Sell leads | iBench - real-time developers Hiring"
                       })

        sleep(200)

    def find_it_company(se):
        se.WD.get(se.url)
        se.WD.maximize_window()
        se.login()
        # se.sleep(3)
        # fill_from(((CLASS, "rw..."), (TAG, "li")), 13)
        # se.Find(XPATH, "//li/a[contains(text(),'Find IT companies')]").out()
        # se.Contains("Find IT companies").out()
        se.Cls("DashboardMenu_menuLink__JkSw7", 3).click()
        se.Cls("Outsource_freeSlot__7mxFS").click()

        # se.Find(NAME, "location").dropdown_multiselect("Afghanistan", "Algeria", "Angola", "Aruba", 25, 0, "Canada", "WTF")#fill_from()   click() #.fill((locators), mode=3)     #click().out()

        se.Find(NAME, "location").dropdown_multiselect()#fill_from()   click() #.fill((locators), mode=3)     #click().out()
        sleep(3)
        se.Find(NAME, "vetted")
        se.sleep(5)
        se.Find(NAME, "name") #.click().type("test1", "test2")
        sleep(5)
        se.Cls("OutsourceAdding_submit__1o3MH")
        sleep(15)

        # se.login()
        # # se.Find(XPATH, "//li/a[contains(text(),'Find IT companies')]").click()
        # # se.Contains("Find IT companies").click()
        # se.Cls("DashboardMenu_menuLink__JkSw7", 3).click()
        # se.curr_url('https://ibench.net/outsource').title("Outsource | iBench - real-time developers Hiring").sleep(3)
        # se.Wait(l_h1).text("Find IT companies")
        # se.Cls("Outsource_freeSlot__7mxFS").click()
        # se.Find(NAME, "vetted").dropdown_select("1").click()
        # se.parent(2).tag("span").attr('class', 'validation_status_ok')
        # se.Find(CLASS, "rw-input-reset").type("United States" + Keys.ENTER + "Canada" + Keys.ENTER)
        # se.Find(NAME, "name").type("Project for QA analysis")
        # se.Find(CLASS, "ql-editor").type("Our project is a software that generates leads and connects companies with professionals")
        # se.Cls("rw-input-reset", 1).type("Information Technology" + Keys.ENTER + "Technology" + Keys.ENTER + Keys.ESCAPE)
        # # se.Contains({"aria-owns":"rw_4_listbox rw_4_notify_area rw_4_taglist"}).type("Information Technology" + Keys.ENTER + "Technology" + Keys.ENTER)
        # se.Contains("Up to $200,000").click()
        # se.Tag("html").elem.send_keys(Keys.PAGE_DOWN)
        # se.Contains("Next Quartal").click()
        # # se.Tag("html").elem.send_keys(Keys.PAGE_DOWN)
        # se.Find(NAME, "links").type('https://www.linkedin.com/')
        # se.Cls("OutsourceAdding_submit__1o3MH").click(action=True)
        # se.sleep(5)
        #
        return




        # sleep(1, 3).click()
        # se.curr_url('https://ibench.net/outsource').title("Outsource | iBench - real-time developers Hiring")
        # se.Wait(l_h1, "Find IT companies")

        sleep(20)

    def main(se):
        se.WD.get(se.url + "registration")  # Get page from WD
        sleep(15)
        se.Contains("type", "password").type("AlexCool2604").attr("value", "AlexCool2604")
        # se.Find(NAME, "password_copy").type("AlexCool2604").attr("value", "AlexCool2604")
        # text_var = se.Xpath('/html/body[1]/div[2]/span[1]/img[1]').text("")
        # se.Find(XPATH, " .....").find(TAG, "a")
        # se.WD.find_element()
        # se.Find().tag()
        # # print(se.elem)
        # # print(se.elems)
        # # se.Cls("FrontPage_skillsLinksContainer__2UBjn").tag("a")
        # # print(se.elem)
        # # print(se.elems)
        # # for se.elem in se.elems:
        # #     se.text().out("text:")
        # #     print(se.out("elem:::"))
        #
        # seelem = se.WD.find_element('xpath', '/html/body[1]/div[2]/span[1]/img[1]')
        # # .img(check=True)
        # # se.Img(check=True)
        # se.Find(XPATH, '/html/body[1]/div[2]/span[1]/img[1]').display()
        # se.Img(check=True)
        se.sleep(20)


if __name__ == "__main__":
    # iBench('Edge').foot_nav_menu()
    iBench().sell_lead()
    # iBench().find_it_company()
    # iBench().head_nav_menu()
    # iBench('Seleniumwire').login()
    # iBench().main()
    # iBench().registration()
    #iBench().recovery_password()
    # iBench().login_cookies()
    print('FINISHED')
    # se = Selen()
    # se.url = "https://www.python.org"
    # se.get()
    # se.sleep(32)