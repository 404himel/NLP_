from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()

driver.get('https://www.techwithtim.net/')

s = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div/div[3]/div/a[1]')
s.send_keys(Keys.RETURN)
i = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div/div[3]/div[1]/div[1]/img')
img = i.get_attribute('src')
print(img)
time.sleep(4)