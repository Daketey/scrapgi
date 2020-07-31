from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import requests
import os
import io
from PIL import Image
import hashlib
import base64

driver_path = 'C:/project/chromedriver'
web_driv = webdriver.Chrome(executable_path = driver_path)

search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=cats&oq=cats&gs_l=img"    ##Replace cats with anything you want to collect images for
web_driv.get(search_url)

image_urls = set()
image_count = 0
number_results = 0

def scroll_to_end(wd, scroll_point):
    web_driv.execute_script(f"window.scrollTo(0, {scroll_point});")
    time.sleep(1)
    
for i in range(1,20):
        scroll_to_end(web_driv, i*1000)
        time.sleep(5)
        thumb = web_driv.find_elements_by_css_selector("img")
        for img in thumb:
            print(img)
            print(img.get_attribute('src'))
            image_urls.add(img.get_attribute('src'))
            image_count = len(image_urls)
            number_results = image_count
            time.sleep(.5)
        print(f"Found: {number_results} search results")
        

folder_path = 'C:/project/Scraper'


for urls in image_urls:
    try:
        image_content = requests.get(urls).content
        print("Successfully downloaded")   
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path=os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10]+'.jpg')
            with open(file_path , 'wb') as f:
                f.write(imgdata)
                print('Successfully Saved')
        except Exception as e:
            print("Couldnt be saved")
        
        
    except Exception as e:
        try:
            urls = urls.split(',')[1]
            base64_bytes = urls.encode('ascii')
            imgdata = base64.b64decode(urls)
            filename = f'C:/games/Scraper/{hashlib.sha1(base64_bytes).hexdigest()[:10]}.jpg'
            with open(filename, 'wb') as f:
                 f.write(imgdata)
            print("Successfully downloaded and Saved")
            
        except Exception as e:
            print("Cannot Download")           
       
   
        
     web_driv.quit()
        
    
        


