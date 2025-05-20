from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.python.org")

time.sleep(2)

link = driver.find_element(By.XPATH,'/html/body/div/header/div/nav/ul/li[2]/a')
download_links = driver.find_elements(By.CSS_SELECTOR, 'ul.subnav.menu li a')

print(link.get_attribute('href'))

for link in download_links:
      print("Text:", link.text.strip())
      print("URL:", link.get_attribute('href'))


time.sleep(6)
