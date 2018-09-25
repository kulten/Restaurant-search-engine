from bs4 import BeautifulSoup
from crawlpack.helpers import id_gen
import json
from crawlpack.helpers import connect

conn, cur = connect()
for count in range(1,425):
    locate = "swiggy/page_source"+str(count)+".html"
    with open(locate,'r') as f:
        soup = BeautifulSoup(f, 'lxml')
        name = soup.find("div", {"class": "OEfxz"}).text.strip()
        address = soup.find("div",{"class": "_1BpLF"})
        full_location = address.contents[0].text
        full_location_temp = full_location.split(',')
        del full_location_temp[1]
        location = ''.join(full_location_temp).strip()
        dedupe_id = id_gen(name,location)
        food = soup.find_all("div", {"class": "GaqmA"})
        item_dict = {}
        for stuff in food:
            item_name = stuff.find("div", {"class": "jTy8b"}).text #gets item name
            item_price = stuff.find("span", {"class": "bQEAj"}).text #gets item price
            item_dict[str(item_name)] = item_price
        items_json = json.dumps(item_dict)
        size = len(item_dict)
        cur.execute("""INSERT INTO swiggy (name,location,dedupe_id,items) VALUES (%s,%s,%s,%s)""",(name,location, dedupe_id ,items_json))
        conn.commit()
        print("Crawled {0}/{1} Items: {2} Restaurant: {3} Location: {4}".format(count,424,size,name,location))
conn.close()
