from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.daraz.com.bd/catalog/?spm=a2a0e.searchlist.0.0.35b6634eUMmpeI&_keyori=ss&from=search_history&q=phone&sugg=phone_3_1')
while True:
    l = driver.find_element(By.CLASS_NAME, 'ant-pagination-item ant-pagination-item-1 ant-pagination-item-active')
    link = l.get_attribute('href')
    print(link)


    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[9]/button'))
        next_button.click()


    except:
        print("No more page")
        break


