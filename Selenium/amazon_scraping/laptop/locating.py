import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()

search = "laptop"
driver.get('https://www.amazon.com/s?k=laptop&crid=VSZ2L9GMB7QD&sprefix=lapto%2Caps%2C403&ref=nb_sb_ss_ts-doa-p_1_5')

element = driver.find_element(By.CLASS_NAME,'puis-card-container')

print(element.get_attribute('outerHTML'))