from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("https://www.facebook.com/login")
time.sleep(3)

driver.find_element(By.ID, 'email').send_keys('***')  
driver.find_element(By.ID, 'pass').send_keys('**')  
driver.find_element(By.NAME, 'login').click()

try:
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "home")]')))
    print("Login successful.")
except Exception as e:
    print("Login may have failed:", e)

post_url = "https://www.facebook.com/TheDailySamakal/posts/pfbid02zgoAGHCKeCy4h3fRjF1VPbmYGWhLDdp1EEobNif1VCmtCwQzqYzAJ6pECPPcHtAbl"
driver.get(post_url)
time.sleep(10)


try:
    for i in range(5):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)
    print("Scrolled through the post and comments.")
except Exception as e:
    print("Scrolling failed:", e)

try:
    replied_count = 0
    checked_indexes = set()
    replied_users = set()

    while replied_count < 3:
        
        reply_buttons = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, '//div[@role="button" and contains(., "Reply")]'
        )))

        for i, reply_button in enumerate(reply_buttons):
            if i in checked_indexes:
                continue

            try:
                print(f"Replying to comment {replied_count + 1}...")

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reply_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", reply_button)
                time.sleep(2)

                reply_box = wait.until(EC.presence_of_element_located((
                    By.XPATH, '//div[@role="textbox" and contains(@aria-label, "Reply to")]'
                )))
                
                aria_label = reply_box.get_attribute("aria-label")
                user_name = aria_label.replace("Reply to ", "").strip()
                if user_name in replied_users: 
                    print(f"Already replied to {user_name}, skipping.")
                    checked_indexes.add(i)
                    continue

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reply_box)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", reply_box)
                time.sleep(1)

                reply_box.send_keys(f"This is automated reply #{replied_count + 1}")
                time.sleep(1)
                reply_box.send_keys(Keys.ENTER)

                
                replied_count += 1
                checked_indexes.add(i)
                time.sleep(3)

                if replied_count == 3:
                    break

            except Exception as inner_e:
                print(f"Could not reply to comment {replied_count + 1}: {inner_e}")
                checked_indexes.add(i)

except Exception as outer_e:
    print("Could not find reply buttons:", outer_e)
input("Press Enter to exit...")
driver.quit()
