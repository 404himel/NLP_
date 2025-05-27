import os
import requests
from bs4 import BeautifulSoup

os.makedirs("saved_img", exist_ok=True)

folder_path = "evaly/data"
img_count = 0

for file in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, file)
        with open(file_path, encoding='utf-8') as f:
            html_file = f.read()

        soup = BeautifulSoup(html_file, 'html.parser')
        i = soup.find(class_="h-[185px]")
        if i:
            img_tag = i.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
                print(f"Downloading: {img_url}")

                response = requests.get(img_url)
                if response.status_code == 200:
                    img_ext = os.path.splitext(img_url)[1].split('?')[0] or ".jpg"
                    img_path = os.path.join("saved_img", f"image_{img_count}{img_ext}")
                    with open(img_path, 'wb') as img_file:
                        img_file.write(response.content)
                    img_count += 1
                else:
                    print(f"Failed to download {img_url}, status code: {response.status_code}")

    except Exception as ex:
        print(f"Error in file {file}: {ex}")
