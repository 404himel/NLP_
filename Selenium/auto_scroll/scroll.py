# scroll effect and collect comment of reviewer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get('https://www.daraz.pk/products/samsung-galaxy-a06-4gb-ram-64-gb-rom-i599915386-s2773207782.html')

height = driver.execute_script('return document.body.scrollHeight')
print(height)
for i in range(0, height, 60):
    driver.execute_script(f'window.scrollTo(0,{i});')
    time.sleep(1)
    c = driver.find_elements(By.CLASS_NAME, 'mod-reviews')
    for j in c:
        with open('/home/himel/Documents/web_scraping/web_scraping/Selenium/auto_scroll/data.txt', 'a', encoding='utf-8') as f:
           f.write(j.text + '\n')
driver.quit()