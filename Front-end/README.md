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

it was like this:
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


