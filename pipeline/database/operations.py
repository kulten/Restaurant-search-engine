import psycopg2


def connect():
    conn = psycopg2.connect(database = "",
                        user = "",
                        password = "",
                        host = "",
                        port = "")
    cur = conn.cursor()
    return conn,cur

def select(dedupe_id,name,cur):
    offset_1 = int(dedupe_id) - 1
    offset_2 = int(dedupe_id) + 1
    cur.execute("SELECT * FROM results WHERE results.dedupe_id = %s OR results.dedupe_id = %s OR results.dedupe_id = %s AND results.name = %s",
        [dedupe_id,offset_1,offset_2 , name])
    count = cur.rowcount
    return count
