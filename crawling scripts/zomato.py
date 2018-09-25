from bs4 import BeautifulSoup
from crawlpack.helpers import id_gen
import json
from crawlpack.helpers import connect

conn, cur = connect()
for count in range(1,3753):
    locate = "zomato_updated/page_source"+str(count)+".html"
    try:
        with open(locate,'r') as f:
            soup = BeautifulSoup(f, 'lxml')
            try:
                stuff = soup.find("div", {"class": "col-m-10"}).find("ol")
                name = stuff.contents[5].text.strip()
                location = stuff.contents[4].text.strip()
                items = soup.find_all("div",{"class":"content"})
                dedupe_id = id_gen(name,location)
                items_final = {}
                for i in items:
                    item_name = i.find("div",{"class":"header"}).text
                    item_raw = i.find("div",{"class":"description"}).text
                    item_price = (item_raw.encode('ascii', 'ignore')).decode("utf-8")
                    items_final[item_name] = item_price
                if len(items_final) == 0:
                    with open("failed_zomato_links.txt","a+") as f:
                        f.write(locate +" ZERO ITEMS " +"\n")
                    print("zero items found")
                else:
                    items_json = json.dumps(items_final)
                    cur.execute("""INSERT INTO zomato (name,location,dedupe_id,items) VALUES (%s,%s,%s,%s)""",(name,location,dedupe_id,items_json))
                    print("Crawled {0}/3752 Restaurant: {1} Items: {2}".format(count,name,str(len(items_final))))
            except:
                with open("failed_zomato_links.txt","a+") as f:
                    f.write(locate +" FAILED " + "\n")
                print("failed")
    except:
        with open("failed_zomato_links.txt","a+") as f:
            f.write(locate +" NOT FOUND " + "\n")
        print("Not found for count ",count)
conn.commit()
print("crawling completed")
conn.close()
