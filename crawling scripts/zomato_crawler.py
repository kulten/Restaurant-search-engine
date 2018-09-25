from crawlpack.helpers import get_information
import time
from selenium import webdriver

def saver(rest, driver, size):
    path = "zomato_updated/page_source"+str(rest)+".html"
    site = "zomato"
    try:
        get_information(rest,size,site,path,driver)
    except:
        time.sleep(10)
        get_information(rest,size,site,path,driver)
    rest = rest + 1
    return rest

urls = []
with open("zomato_links.txt", "r") as ins:
    for line in ins:
        urls.append(line)

rest = 1
driver = webdriver.Chrome()
size = str(len(urls))
for link in urls:
    if cw >= 100 and cw%100 == 0:
        driver.quit()
        time.sleep(20)
        driver = webdriver.Chrome()
        driver.get(link)
        rest = saver(rest, driver, size)
    else:
        driver.get(link)
        rest = saver(rest, driver, size)
