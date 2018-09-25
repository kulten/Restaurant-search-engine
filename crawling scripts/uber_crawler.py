from crawlpack.helpers import get_information
import time
from selenium import webdriver

urls = []
with open("uber_links.txt", "r") as ins:
    for line in ins:
        urls.append(line)

cw = 1
driver = webdriver.Chrome()
size = str(len(urls))
for link in urls:
    url = "https://www.ubereats.com/en-IN" + link
    driver.get(url)
    path = "uber_eats/page_source"+str(cw)+".html"
    site = "uber eats"
    try:
        get_information(cw,size,site,path,driver)
    except:
        time.sleep(10)
        get_information(cw,size,site,path,driver)
    cw = cw + 1
