from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

driver = webdriver.Chrome()

path = '/home/himel/Documents/web_scraping/Daraz_scraping/scaraping'
data_path = os.path.join(path,'data','keyboard')
os.makedirs(data_path, exist_ok=True)



for page in range(1,20):
    driver.get(f"https://www.amazon.com/s?k=keyboard&page={page}&xpid=3Sckie4D4fyRb&crid=2WRY1YNVRFYYM&qid=1747807621&sprefix=keybo%2Caps%2C367&ref=sr_pg_1")

    infos = driver.find_elements(By.CLASS_NAME,'puis-card-container')


    for id,info in enumerate(infos):
       data = info.get_attribute('outerHTML')
       file_path = os.path.join(data_path, f"{id}.html")
       with open(file_path,"w", encoding='utf-8') as f:
            f.write(data)

time.sleep(1)
driver.close()
