import time
from selenium import webdriver
import json
from crawlpack.helpers import id_gen, connect



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
driver = webdriver.Chrome(chrome_options=chrome_options)
conn, cur = connect()
for count in range(1,89):
    try:
        url = "file:///home/Desktop/crawler%20scripts/scripts/uber_eats/page_source"+str(count)+".html"
        driver.get(url)
        raw_title = driver.find_element_by_xpath('//*[@id="app-content"]/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div/div/h1').text
        try:
            split_title = raw_title.split('-')
            rest_name = split_title[0].strip()
            location = split_title[1].strip()
        except:
            rest_name = raw_title
            location = "Bangalore"
        dedupe_id = id_gen(rest_name,location)
        items = driver.find_elements_by_css_selector('#app-content>div>div>div:nth-child(1)>div>div:nth-child(1)>div:nth-child(2)>div>div:nth-child(3)>div:nth-child(2)>div:nth-child(1)>div>div:nth-child(2)>div>div>div>div:nth-child(1)>div:nth-child(1)')
        prices = driver.find_elements_by_css_selector('#app-content>div>div>div:nth-child(1)>div>div:nth-child(1)>div:nth-child(2)>div>div:nth-child(3)>div:nth-child(2)>div:nth-child(1)>div>div:nth-child(2)>div>div>div>div:nth-child(1)>div:nth-child(3)>span:nth-child(1)')
        items_final = {}
        num_items = len(items)
        for i in range(0,num_items):
            item_price = prices[i].text.replace("INR","")
            item_name = items[i].text
            items_final[item_name] = item_price
        items_json = json.dumps(items_final)
        cur.execute("""INSERT INTO uber_eats2 (name,location,items) VALUES (%s,%s,%s)""",(rest_name,location,items_json))
        conn.commit()
        print("Crawled {0}/88 Restaurant: {1} Items: {2}".format(count,rest_name,str(len(items_final))))
    except:
        print("error ",url)
