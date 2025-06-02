from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get('https://www.google.com/maps/search/laptop+shop+near+me/@23.4160898,91.1407087,12z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI1MDUyOC4wIKXMDSoASAFQAw%3D%3D')


height = driver.execute_script('return document.body.scrollHeight')
scrollable = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]'))
)

for i in range(height):
    driver.execute_script("arguments[0].scrollTop += 500;", scrollable)
    time.sleep(1)

locations = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.Nv2PK'))
)

results = []

for loc in locations:
    try:
        shop_name = loc.find_element(By.CSS_SELECTOR, '.qBF1Pd').text
    except:
        shop_name = None

    try:
        review = loc.find_element(By.CSS_SELECTOR, '.MW4etd').text
    except:
        review = None

    try:
        location = loc.find_element(By.CSS_SELECTOR, '.W4Efsd').text
    except:
        location = None

    try:
        phone_number = loc.find_element(By.CSS_SELECTOR, '.UsdlK').text
    except:
        phone_number = None

    try:
        img = loc.find_element(By.CSS_SELECTOR, '.FQ2IWe img')
        img_url = img.get_attribute('src')
    except:
        img_url = None

    results.append({
        'shop_name': shop_name,
        'Review': review,
        'Location': location,
        'Number': phone_number,
        'img': img_url
    })

df = pd.DataFrame(results)
df.to_csv('laptop_shop_data.csv', index=False)
print("Data saved successfully.")
driver.quit()
