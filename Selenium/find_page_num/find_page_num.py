from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


driver = webdriver.Chrome()
driver.get('https://www.aliexpress.com/w/wholesale-ac.html?page=60&g=y&SearchText=ac')

time.sleep(10)

l = driver.find_element(By.CLASS_NAME,'comet-pagination')
data = l.get_attribute('outerHTML')
with open(os.path.join("find_page_num/data","outer.html")) as f:
    f.write(data)
print(l)
