from crawlpack.helpers import get_information
import time
from selenium import webdriver

urls = []
with open("swiggy_links.txt", "r") as ins:
    for line in ins:
        urls.append(line)

count = 1
driver = webdriver.Chrome()
size = str(len(urls))
for link in urls:
    driver.get(link)
    path = "swiggy/page_source"+str(cw)+".html"
    site = "swiggy"
    try:
        get_information(cw,size,site,path,driver)
    except:
        time.sleep(10)
        get_information(cw,size,site,path,driver)
    count = count + 1
