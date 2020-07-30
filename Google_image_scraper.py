from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time

driver_path = 'C:/games/chromedriver'
web_driv = webdriver.Chrome(executable_path = driver_path)

search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=cats&oq=cats&gs_l=img"
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


