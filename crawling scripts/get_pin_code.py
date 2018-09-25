import requests
import json
from psycopg2 import sql
from crawlpack.helpers import connect

default = ",bangalore,india"
api_key = ""
conn, cur = connect()
tables = ["swiggy","uber_eats2","zomato"]
for table in tables:
    cur.execute(sql.SQL("SELECT id,name,location,lat_long FROM {}").format(sql.Identifier(table)))
    rows = cur.fetchall()
    row_count = cur.rowcount
    count = 1
    for row in rows:
        id = row[0]
        name = row[1]
        location = row[2]
        lat_long = row[3]
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+lat_long+'&key='+api_key)
        json_items = response.json()
        try:
            pin_code = int(json_items['results'][0]['address_components'][-1]['short_name'])
        except:
            pin_code = 0
        cur.execute(sql.SQL("UPDATE {} SET dedupe_id = %s WHERE id = %s").format(sql.Identifier(table)),[pin_code,id])
        print("updated {0}/{1} for {2}".format(count,row_count,table))
        count = count + 1
    conn.commit()
