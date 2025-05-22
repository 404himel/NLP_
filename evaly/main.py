import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
search = "headphone"
file = 0


os.makedirs("evaly/data", exist_ok=True)

for page in range(1, 5):
    driver.get(f"https://evaly.com.bd/search?page={page}&term={search}")
    time.sleep(3)  

    elements = driver.find_elements(By.CLASS_NAME, 'bg-white.border.rounded-md')
    print(f"Page {page}: Found {len(elements)} elements.")

    for element in elements:
        data = element.get_attribute("outerHTML")
        with open(os.path.join("evaly/data", f"{search}_{file}.html"), "w", encoding="utf-8") as f:
            f.write(data)
        file += 1

driver.close()
