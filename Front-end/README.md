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

### simplified adding locators to methods by several variants
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

### Find and find is different method
Methods `Find` with Capitalise name used if it calls first after the WebDriver (for All WEB page elements) and the lowercase method `find` is used when calling after another already found element.
There are several more methods that work in the same principle. But more on that later.
