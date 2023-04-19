# SELEN 
this is a mini framework or an add-on for the selenium and unitest frameworks

## Basic goals

- making it easier to write code of tests
- improving code readability
- to reduce the amount of code written
- accelerating the development of tests based on selenium and unittest frameworks
- error reduction


# Quick stars and understanding

## So, what can Selen do:

### New find method and simplified adding locators as method arguments

It was like this:
```python

driver.find_element(By.ID, "id")
driver.find_element(By.NAME, "name")
driver.find_element(By.XPATH, "xpath")
driver.find_element(By.LINK_TEXT, "link text")
driver.find_element(By.PARTIAL_LINK_TEXT, "partial link text")
driver.find_element(By.TAG_NAME, "tag name")
driver.find_element(By.CLASS_NAME, "class name")
driver.find_element(By.CSS_SELECTOR, "css selector")

```
Now is:
```pyhton
se.Find(ID, "id")
se.Find(NAME, "name")
se.Find(XPATH, "xpath")
se.Find(LINK, "link text")
se.Find(PART_LINK, "partial link text")
se.Find(TAG, "tag name")
se.Find(CLASS, "class name")
se.Find(CSS, "css selector")
```
******* `se` it is short from `self`

### Simplified adding locators to methods by several variants
It Was like:
```python
driver.find_element(By.XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
driver.find_element(By.CLASS_NAME, ""Login_submit_wrapper__2-PYe"")

#or
driver.find_element("xpath", "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
driver.find_element("class name", ""Login_submit_wrapper__2-PYe"")

#or with locator variables
xpath_locator = ("xpath", "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = ("class_name", "Login_submit_wrapper__2-PYe"")

driver.find_element(*xpath_locator)
driver.find_element(class_locator[0], class_locator[1])
```
With Selen is:
```python
se.Find(XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
se.Find(CLASS, ""Login_submit_wrapper__2-PYe"")

#or with locator variables
xpath_locator = (XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = (CLASS, "Login_submit_wrapper__2-PYe"")

se.Find_element(xpath_locator)
se.Find_element(class_locator)
```

### `Find` and `find` are differents method
Methods `Find` with Capital first letter used if it calls first after the WebDriver (for All WEB page elements) and the lowercase method `find` is used when calling after another already found element.
There are several more methods that work in the same principle. But more on that later.

It Was like:
```python
driver.find_element(By.XPATH, "//xpath string...").find_element(By.CLASS_NAME, Login_submit_wrapper__2-PYe)

#or with locator variables
xpath_locator = ("xpath", "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = ("class_name", "Login_submit_wrapper__2-PYe"")
tag_locator = ("tag name", "input")

driver.find_element(*xpath_locator).find_element(*class_locator).find_element(*tag_locator)
```
Now with Selen:
```python
se.Find(XPATH, "//xpath string...").find(CLASS, "Login_submit_wrapper__2-PYe)

#or with locator variables
xpath_locator = (XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = (CLASS, "Login_submit_wrapper__2-PYe)
tag_locator = (TAG, "input")

se.Find(xpath_locator).find(class_locator).find(tag_locator)
```
## Even shorter code in method chains to find elements
Several ways to search for elements by a chain of locators, all locators in one `Find` method  
```python
# all locator as tuples inside one method 
se.Find((XPATH, "//xpath string..."),(By.CLASS, "Login_submit_wrapper__2-PYe))

#or with locator variables
xpath_locator = (XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = (CLASS, "Login_submit_wrapper__2-PYe)
tag_locator = (TAG, "input")

se.Find(xpath_locator, class_locator, tag_locator)

#or All locators in one variable : Tuple of tuples
locators = ((XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]"),
            (CLASS, "Login_submit_wrapper__2-PYe),
            (TAG, "input"))

se.Find(locators)

#or Combined addition of locators  
se.Find(locators, xpath_locator, (TAG, "a"))
se.Find((Tag, "a"), xpath_locators, locators)
# ! Any combinations as You wish
```

## Method `Wait` - finding and waiting for the appearance of an element on the page and not only
The method `Wait` can take the same parameters as the `Find` method, but it will only expect the first element in the chain and the rest of the elements in the chain will be found in the same way as the find method does.
- No exception handling is required, the logic is already inside the White method
It was like:
```pyhton
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
except:
    driver.quit()
```
Now with Selen examples:
```python

from selen import *

se.Wait(ID, "myDynamicElement")

se.Wait(ID, "myDynamicElement").find(CLASS, "Login_submit_wrapper__2-PYe)

#or with locator variables
id_locator = (ID, "MyDynamicElement")
class_locator = (CLASS, "Login_submit_wrapper__2-PYe)
tag_locator = (TAG, "input")

se.Wait(xpath_locator).find(class_locator).find(tag_locator)

# all locator as tuples inside one method 
se.Wait((XPATH, "//xpath string..."),(By.CLASS, "Login_submit_wrapper__2-PYe))

#or with locator variables
xpath_locator = (XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]")
class_locator = (CLASS, "Login_submit_wrapper__2-PYe)
tag_locator = (TAG, "input")

se.Wait(xpath_locator, class_locator, tag_locator)

#or All locators in one variable : Tuple of tuples
locators = ((XPATH, "//body/div[@id='fb-root']/div[@id='root']/div[1]/div[1]/div[2]/div[1]"),
            (CLASS, "Login_submit_wrapper__2-PYe),
            (TAG, "input"))

se.Wait(locators)

#or Combined addition of locators  
se.Wait(locators, xpath_locator, (TAG, "a"))
se.Wait((TAG, "a"), xpath_locators, locators)
# ! Any combinations as You wish
```
