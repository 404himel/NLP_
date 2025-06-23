from bs4 import BeautifulSoup
import os
import pandas as pd

a=1

dir = {
    'title':[],
    'rating':[],
    'img':[]
}

for file in os.listdir("scaraping/data/keyboard"):
    try:
        with open(f"scaraping/data/keyboard/{file}",encoding="utf-8") as f:
            data = f.read()
        soup = BeautifulSoup(data, "html.parser")

        t = soup.find(class_="a-size-medium a-spacing-none a-color-base a-text-normal")
        title = t.get_text()
        

        r = soup.find(class_="a-icon-alt")
        rating = r.get_text()
        

        i = soup.find(class_="a-section aok-relative s-image-fixed-height")
        im = i.find('img')
        img = im['src']
        
        
        dir['title'].append(title)
        dir['img'].append(img)
        dir['rating'].append(rating)
        
    except Exception as ex:
        print(ex)
    
df = pd.DataFrame(data=dir)
df.to_csv("AmazonKeyboardData.csv")