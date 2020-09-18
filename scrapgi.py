#!/usr/bin/env python
# coding: utf-8

# In[24]:


from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import base64
import requests
import cv2
import os
import io
from PIL import Image
import hashlib
import numpy as np


# In[36]:


def call_from_browser(Search_word , Driver_path, amount_data):
    
    def scroll_to_end(web_driv, scroll_point):
        web_driv.execute_script(f"window.scrollTo(0, {scroll_point});")
        time.sleep(1)
    
    web_driv = webdriver.Chrome(executable_path = Driver_path)

    search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={Search_word}&oq={Search_word}&gs_l=img"

    web_driv.get(search_url)

    image_urls = set()
    image_count = 0
    number_results = 0

    for i in range(1,20):
        scroll_to_end(web_driv, i*100)
        time.sleep(5)
        thumb = web_driv.find_elements_by_css_selector("img")
        for img in thumb:
            image_urls.add(img.get_attribute('src'))
            image_count = len(image_urls)
            number_results = image_count
            if(number_results==amount_data+1):
                web_driv.quit()
                return image_urls   
            time.sleep(.5)
            print(f"Found: {number_results} search results.")
        

def save_image(folder_path , image_urls):

    for urls in image_urls:
        try:
            image_content = requests.get(urls).content
            print("Successfully downloaded")

            try:
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')
                file_path=os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10]+'.jpg')
                with open(file_path , 'wb') as f:
                    image.save(f, "JPEG", quality=85)
                    print('Successfully Saved')
            
            except:
                print("Couldnt be saved")  


        except: 
            try:
                urls = urls.split(',')[1]
                base64_bytes = urls.encode('ascii')
                imgdata = base64.b64decode(urls)
                filename = f'{folder_path}/{hashlib.sha1(base64_bytes).hexdigest()[:10]}.jpg'

                with open(filename, 'wb') as f:
                    f.write(imgdata)
                    print("Successfully Saved")  
                        
            except:
                print("Couldnt be saved")  


# In[53]:


def create_traindata(Directory , labels):
    tranning_data=[]
    for label in labels:
        img_path = os.path.join(Directory , label)
        label_index = labels.index(label)
        for img in os.listdir(img_path):
            try:
                img_array = cv2.imread(os.path.join(img_path,img) , cv2.IMREAD_GRAYSCALE)
                new_img_array = cv2.resize(img_array,(100,100))
                tranning_data.append([new_img_array, label_index])
            except:
                pass 
    
    return tranning_data

