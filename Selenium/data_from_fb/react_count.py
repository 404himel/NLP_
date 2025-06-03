from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup



with open('/home/himel/Documents/web_scraping/web_scraping/from_fb/outer.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

r = soup.find_all(class_='x193iq5w')

for i,j in enumerate(r):
    if i == 1:
        print("Total Love React: ",j.text)
    elif i == 2:
        print("Total Like React: ",j.text)
    elif i == 3:
        print("Total Care React: ",j.text)
    elif i == 4:
        print("Total wow react: ",j.text)
    