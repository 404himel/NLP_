from bs4 import BeautifulSoup
import os

file = "/home/himel/Documents/web_scraping/web_scraping/find_page_num/data/outer.html"

with open(file, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser') 

t = soup.find(class_="comet-pagination-item comet-pagination-item-60 comet-pagination-item-active")

if t:
    total_page = t.text
    print("Total page:", total_page)
else:
    print("Pagination element not found.")


#iterate all page using loop
for i in range(1,int(t.text)+1):
    print(i)
