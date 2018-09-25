import requests
import json
import time
import itertools
from crawlpack.helpers import connect


urls = []
conn, cur = connect()
with open("correct_zomato_links.txt","r") as reader:
    for line in reader:
        urls.append(line)
seq = ["key1","key2",
       "key3","key4",
       "key5","key6"]
offset = 0
length = len(urls) + offset
round_robin = itertools.cycle(seq)
https_proxy = "https://103.250.166.16:37148"
proxyDict = {"https" : https_proxy}
count = offset
for link in urls:
    temp = ""
    for i in link:
        if i.isdigit():
            temp = temp + i
    api_key = next(round_robin)
    headers = {
    'Accept': 'application/json',
    'user-key': api_key,
            }

    params = (('res_id', temp),)
    response = requests.get('https://developers.zomato.com/api/v2.1/restaurant', headers=headers, params=params,proxies=proxyDict)
    json_items = json.loads(response.text)
    db_info = json.dumps(json_items)
    try:
        name = json_items["name"]
        location = json_items["location"]["locality"]
        latitude = json_items["location"]["latitude"]
        longitude = json_items["location"]["longitude"]
        final_lat_long = latitude + "," + longitude
        cur.execute("UPDATE zomato SET lat_long = %s, full_details = %s WHERE name = %s AND location = %s", [final_lat_long,db_info, name, location])
        conn.commit()
        print("{0}/{1} {2} {3}".format(count,length,name,location))
        count = count + 1
    except:
        print("Failed ",link)
        count = count + 1
        with open("failed_zomato_links.txt","a") as f:
            f.write(link + "\n")
    time.sleep(1)
