import requests
import json
from psycopg2 import sql
from crawlpack.helpers import connect

api_key = ""
conn, cur = connect()
tables = ["swiggy","uber_eats2"]
for table in tables:
    cur.execute(sql.SQL("SELECT id,name,location FROM {}").format(sql.Identifier(table)))
    number_of_rows = cur.rowcount
    rows = cur.fetchall()
    count = 1
    for row in rows:
        id = row[0]
        name = row[1]
        location = row[2]
        address = name +","+location
        try:
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+api_key)
            json_items = response.json()
            db_items = json.dumps(json_items)
            geocode = json_items["results"][0]["geometry"]["location"]
            latitude = str(geocode["lat"])
            longitude = str(geocode["lng"])
            final = latitude + "," + longitude
            cur.execute(sql.SQL("UPDATE {} SET lat_long= %s, full_details = %s WHERE id = %s").format(sql.Identifier(table)),[final,db_items, id])
            print("{0}/{1} updated {2}".format(count,number_of_rows,name))
        except:
            print("failed for id: {0} name: {1} in table: {2}".format(id,name,table))
        count = count + 1
    conn.commit()
