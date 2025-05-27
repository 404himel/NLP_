from bs4 import BeautifulSoup
import os
import pandas as pd

data = {
    'title':[],
    'price':[],
    'link':[],
    'img':[],
    'rating':[],
    'num_rating':[],
    'bought':[]
    }



for file in os.listdir("Selenium/amazon"):
    try:
        with open(f"Selenium/amazon/{file}", encoding='utf-8') as f:
            html_file = f.read()
        soup = BeautifulSoup(html_file, 'html.parser')

        # Title
        t = soup.find("h2")
        title = t.get_text(strip=True) if t else None
        data['title'].append(title)

        # Price
        p = soup.find(class_="a-price-whole")
        price = p.get_text(strip=True) if p else None
        data['price'].append(price)

        # Link
        link = None
        l = soup.find(class_='aok-relative')
        if l:
            a_tag = l.find('a')
            if a_tag and 'href' in a_tag.attrs:
                link = 'https://amazon.com' + a_tag['href']
        data['link'].append(link)

        # Image
        img = None
        i = soup.find(class_='a-section aok-relative s-image-fixed-height')
        if i:
            img_tag = i.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img = img_tag['src']
        data['img'].append(img)

        # Rating
        r = soup.find("span", class_="a-icon-alt")
        rating = r.get_text(strip=True) if r else None
        data['rating'].append(rating)

        # Number of ratings
        n = soup.find("span", class_="a-size-base s-underline-text")
        num_rating = n.get_text(strip=True) if n else None
        data['num_rating'].append(num_rating)

        # Bought
        b = soup.find("span", class_="a-size-base a-color-secondary")
        bought = b.get_text(strip=True) if b else None
        data['bought'].append(bought)

    except Exception as ex:
        print(f"Error in file {file}: {ex}")

df = pd.DataFrame(data=data)
df.to_csv("amazon_laptop_data.csv", index=False, encoding='utf-8')