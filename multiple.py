import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

driver = webdriver.Chrome()
search = "laptop"
file = 0

for page in range(1, 10):
    driver.get(f"https://www.amazon.com/s?k=laptop&page={page}&xpid=FDep6LU0NAQUg&crid=VSZ2L9GMB7QD&qid=1747746746&sprefix=lapto%2Caps%2C403&ref=sr_pg_2")

    elements = driver.find_elements(By.CLASS_NAME,'puis-card-container')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'amazon')
    os.makedirs(output_dir, exist_ok=True) 

    for element in elements:
        data = element.get_attribute("outerHTML")
        with open(os.path.join(output_dir, f"{search}_{file}.html"),"w",encoding='utf-8') as f:
            f.write(data)
            file+=1

    time.sleep(1)
driver.close()