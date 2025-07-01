from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

author = {
    'author_name': [],
    'Followers': []
}

book_info = {
    'Title': [],
    'Product_summary': [],
    'Original_Price': [],
    'Offer_Price': [],
    'Rating': []
}

Reviews = {
    'Book_Title': [],
    'Reviews': []
}

author_links = []

def fast_scroll(driver):
    scroll_pause_time = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def slow_scroll(driver):
    scroll_step = 200
    delay = 0.4
    current_height = 0
    total_height = driver.execute_script("return document.body.scrollHeight")
    while current_height < total_height:
        current_height += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(delay)

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


def process_author_link(author_link, thread_id):
    driver = create_driver()
    try:
        print(f"Thread {thread_id}: Scraping Author {author_link}")
        driver.get(author_link)
        time.sleep(2)
        fast_scroll(driver)

        try:
            total_book_div = driver.find_element(By.CSS_SELECTOR, '.browse__content--heading')
            p_tag = total_book_div.find_element(By.TAG_NAME, 'p')
            total_book_text = p_tag.text
            print(f"Thread {thread_id}: {total_book_text}")
            matches = re.findall(r'\d+', total_book_text)
            total_items = int(matches[-1]) if matches else 0
            print(f"Thread {thread_id}: Total books: {total_items}")
        except Exception as e:
            print(f"Thread {thread_id}: Could not find book count: {e}")
            total_items = 0

        for i in range(total_items):
            try:
                time.sleep(1)
                books = driver.find_elements(By.CSS_SELECTOR, '.books-wrapper__item')
                if i >= len(books):
                    print(f"Thread {thread_id}: Index {i} out of range. Skipping.")
                    continue

                button = books[i].find_element(By.CSS_SELECTOR, '.home-details-btn-wrapper a')
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", button)

                print(f"Thread {thread_id}: Book {i+1} button clicked")

                slow_scroll(driver)

                # book title
                try:
                    book_title = driver.find_element(By.CSS_SELECTOR, 'h1').text.strip()
                    print(f"Thread {thread_id}: Book Title: {book_title}")
                except:
                    print(f"Thread {thread_id}: Could not get book title")
                    book_title = "N/A"
                book_info['Title'].append(book_title)

                # Product Summary
                try:
                    description = driver.find_element(By.CSS_SELECTOR, '.productSummary_summeryText__Pd_tX').text
                except:
                    print(f"Thread {thread_id}: Error in Description")
                    description = "N/A"
                book_info['Product_summary'].append(description)

                # rating
                try:
                    rating = driver.find_element(By.CSS_SELECTOR, '.detailsReviewHeader_ratingSummary___aFy_ h3').text
                    print(f"Thread {thread_id}: {rating}")
                except:
                    print(f"Thread {thread_id}: Error in rating")
                    rating = "N/A"
                book_info['Rating'].append(rating)

                # Reviews
                try:
                    for j in range(2):
                        try:
                            more_reviews_button = driver.find_element(By.XPATH, "//div[@class='text-center border-y border-[#f1f1f1] py-4']//button[contains(text(), 'Show more Reviews')]")
                            driver.execute_script("arguments[0].click();", more_reviews_button)
                            time.sleep(2)
                        except:
                            print(f"Thread {thread_id}: Error in more_review")
                            break
                    review_c = driver.find_element(By.CSS_SELECTOR, '.cardContainer_frontProductList__TP9Eo.cardContainer_reviewSectionContainer__TmIwS')
                    review_blocks = review_c.find_elements(By.CLASS_NAME, 'singleReview_reviewComment__gKQY8')
                    for idx, block in enumerate(review_blocks, 1):
                        try:
                            review = block.find_element(By.XPATH, ".//div[contains(@class, 'text-[14px]')]").text.strip()
                            Reviews['Book_Title'].append(book_title)
                            Reviews['Reviews'].append(review)
                        except Exception as e:
                            print(f"Thread {thread_id}: Error extracting review {idx}: {e}")
                except:
                    print(f"Thread {thread_id}: Error In Review")

                # Price
                try:
                    price_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.priceDetails_priceAndDiscount__oEFMK'))
                    )
                    try:
                        original_price = price_div.find_element(By.CSS_SELECTOR, '.original-price').text
                    except:
                        original_price = "N/A"
                    try:
                        selling_price = price_div.find_element(By.CSS_SELECTOR, '.sell-price').text
                    except:
                        try:
                            selling_price = price_div.find_element(By.CSS_SELECTOR, '.price').text
                        except:
                            selling_price = "N/A"
                except:
                    print("Thread {thread_id}: Could not find price section")
                    original_price = "N/A"
                    selling_price = "N/A"

                book_info['Original_Price'].append(original_price)
                book_info['Offer_Price'].append(selling_price)

                driver.back()
                time.sleep(2)

            except Exception as e:
                print(f"Thread {thread_id}: Error at book index {i}: {e}")
                try:
                    driver.back()
                    time.sleep(2)
                except:
                    pass

    except Exception as e:
        print(f"Thread {thread_id}: Error processing author: {e}")
    finally:
        driver.quit()

def main():
    author_links=[]
    for page_num in range(1,2):
        driver = create_driver() #Customized the Chrome
        try:
            url = f"https://www.rokomari.com/book/authors?ref=sm_p0&page={page_num}"
            print(f"Scraping Page {page_num}")
            driver.get(url)
            time.sleep(1)
            fast_scroll(driver)

            authors_section = driver.find_element(By.CSS_SELECTOR, '.all-authors-section')
            author_list_items = authors_section.find_elements(By.CSS_SELECTOR, '.authorListItem')

            for idx, author_item in enumerate(author_list_items):
                try:
                    author_link = author_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    author_links.append(author_link)
                    author_name = author_item.find_element(By.CSS_SELECTOR,'.small-sized-text.text-center.name-text-container').text.strip()
                    author['author_name'].append(author_name)
                    print(author_name)
                    followers = author_item.find_element(By.CSS_SELECTOR,'.primary-text-color.js--follower-count').text.strip()
                    author['Followers'].append(followers)

                except Exception as e:
                    print(f"Page {page_num}: Error collecting author link {idx+1}: {e}")
            author_links = author_links[:1]
                
        except Exception as e:
            print(f"Page {page_num}: Error loading page: {e}")
        finally:
            driver.quit()

    print(f"Total authors collected: {len(author_links)}")

    # Process authors in multithread
    max_threads = 3
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for idx, link in enumerate(author_links):
            thread_id = (idx % max_threads) + 1
            future = executor.submit(process_author_link, link, thread_id)
            futures.append(future)
            time.sleep(1)

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Thread completed with error: {e}")

    # Save CSVs
    try:
        pd.DataFrame(author).to_csv('authors_arif_azad.csv', index=False)
        print("Saved authors.csv")
        pd.DataFrame(book_info).to_csv('books_arif_azad.csv', index=False)
        print("Saved books.csv")
        pd.DataFrame(Reviews).to_csv('reviews_arif_azad.csv', index=False)
        print("Saved reviews.csv")
    except Exception as e:
        print(f"Error saving CSV files: {e}")

if __name__ == "__main__":
    main()
