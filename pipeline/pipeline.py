from psycopg2 import sql
import time
from jsonops.restops import create_new_entry, update_existing_entry,format_data
from database.operations import connect,select


# Healthie
# Mama Mia!
# Masala Oota
# Green Theory

conn, cur = connect()
while(True):
        tables = ["swiggy","uber_eats2","zomato"]
        for table in tables:
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
            rows = cur.fetchall()
            count = 0
            if table == "swiggy":
                site = "swiggy"
            elif table == "uber_eats2":
                site = "uber eats"
            elif table == "zomato":
                site = "zomato"
            for row in rows:
                name, location, dedupe_id,cur_items,lat_long = format_data(row,table)
                row_count = select(dedupe_id,name,cur)
                if row_count == 0:
                    json_items = create_new_entry(cur_items,"zomato","uber eats","swiggy",site)
                    cur.execute("INSERT INTO results (name,location,dedupe_id,items,lat_long) VALUES (%s,%s,%s,%s,%s)", [name, location, dedupe_id, json_items,lat_long])
                else:
                    selected = cur.fetchall()
                    json_items, id = update_existing_entry(selected, cur_items,"zomato","uber eats","swiggy",site)
                    cur.execute("UPDATE results SET items = %s,lat_long = %s WHERE id = %s", [json_items, lat_long,id])
                count = count + 1
                print(count)
            conn.commit()
            print("Ran Pipeline for ", table)
        time.sleep(5)