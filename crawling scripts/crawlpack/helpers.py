import time
from psycopg2 import connect

def get_information(cw,size,name,path,driver):
    time.sleep(3)
    source = driver.page_source
    with open(path, "w") as f:
        f.write(source)
    print("Crawled {0}/{1} from {2}".format(cw,size,name))
    time.sleep(13)

def id_gen(name,location):
    name_norm = name.replace(" ","").lower()
    location_norm = location.replace(" ","").lower()
    dedupe_id_raw = name_norm + location_norm
    dedupe_id_clean = dedupe_id_raw.replace(".","")
    return dedupe_id_clean

def connect():
    conn = connect(database = "",
                   user = "",
                   password = "",
                   host = "",
                   port = "")
    cur = conn.cursor()
    return conn,cur
