# ibench.py

## How it works

The `iBench` class extends the `Selen` class from the `selen` module to create a web automation script for the iBench website. The class includes methods to navigate the website, log in, and perform other actions.

The class initializes with the `url` property set to the iBench website and `ok_assertions` and `ok_print` properties set to `False` and `True` respectively.

The `main_page()` method navigates to the iBench website and checks for the presence of the page title, URL, and header text. It also prints the status of links and images on the page.

The `login()` method logs into the website using the provided email and password. It first navigates to the login page and checks for the presence of the correct header text and URL. It then enters the email and password into the login form, checks for validation, and submits the form. Finally, it checks that the user is redirected to the correct page.

The `login_cookies()` method logs into the website using cookies.

The `registration()` and `recovery_password()` methods are placeholders for future functionality.

The `main()` method closes the browser window.

## Usage

To use the script, simply run the `login` method of the `iBench` class:

```python
from ibench import iBench

if __name__ == "__main__":
    iBench().login()
```

Make sure to provide the correct email and password in the `security` module.# positive_tests.py

## Description

This script contains four test cases that verify the login functionality of a website on different web browsers. The test cases are implemented using Python's unittest module and iBench library.

## How it works

1. The script imports the unittest module and iBench library.
2. Four test case classes are defined for Chrome, Firefox, Edge, and Opera web browsers, respectively. Each test case class inherits from the unittest.TestCase class.
3. A setUp method is defined for each test case class to initialize an iBench object with the respective web browser.
4. A test_login method is defined for each test case class to call the login method of the iBench object.
5. A tearDown method is defined for each test case class to close the web driver and set the iBench object to None.

## Usage

To run the test cases, execute the following command:

```
python positive_tests.py
```

Note: Make sure to have iBench and the respective web drivers installed and added to the system PATH.