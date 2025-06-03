from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

data = {
    'Name': [],
    'Id_url': [],
    'comment': []
}

with open('/home/himel/Documents/web_scraping/web_scraping/from_fb/comment_outer.html', 'r', encoding='utf-8') as f:
    html_con = f.read()

soup = BeautifulSoup(html_con, 'html.parser')

names = soup.find_all(class_='x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1nxh6w3 x1sibtaa x1s688f xzsf02u')
comments = soup.find_all(class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs')
id_links = soup.find_all(class_='x16hk5td x12rz0ws')

# Loop through minimum length to avoid mismatch
for i in range(min(len(names), len(comments), len(id_links))):
    name_text = names[i].get_text(strip=True)
    comment_text = comments[i].get_text(strip=True)
    
    a_tag = id_links[i].find('a')
    if a_tag and a_tag.has_attr('href'):
        base = a_tag['href'].split('?')[0]
    else:
        base = ''

    data['Name'].append(name_text)
    data['comment'].append(comment_text)
    data['Id_url'].append(base)

df = pd.DataFrame(data)
df.to_csv('users.csv', index=False)
print('Saved')
