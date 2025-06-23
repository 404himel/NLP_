from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://www.techwithtim.net/tutorials')


g = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div/div[3]/div[1]/div[2]/div[2]/a')
g.click()

try:
    
    t = WebDriverWait(g, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div/div[2]/div[2]')))
    print(t.text)

finally:
    driver.quit()