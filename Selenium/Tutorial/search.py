from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()

driver.get('https://www.techwithtim.net/')
print(driver.title)

s = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div/div[3]/div/a[1]')
s.send_keys(Keys.RETURN)
time.sleep(4)