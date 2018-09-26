import json


def create_new_entry(cur_items,rest_1,rest_2,rest_3,cur_rest):
    item = {}
    for dish in cur_items :
        item[dish] = {}
        item[dish][rest_1] = "N/A"
        item[dish][rest_2] = "N/A"
        item[dish][rest_3] = "N/A"
        item[dish][cur_rest] = cur_items[dish]
    json_items = json.dumps(item)
    return json_items

def update_existing_entry(selected,cur_items,rest_1,rest_2,rest_3,cur_rest):
    raw_selected = selected[0]
    item = raw_selected[4]
    id = int(raw_selected[0])
    for dish in cur_items :
        if dish in item :
            item[dish][cur_rest] = cur_items[dish]
        else :
            item[dish] = {}
            item[dish][rest_1] = "N/A"
            item[dish][rest_2] = "N/A"
            item[dish][rest_3] = "N/A"
            item[dish][cur_rest] = cur_items[dish]
    json_items = json.dumps(item)
    return json_items, id

def format_data(row,table):
    name = str(row[1])
    location = str(row[2])
    dedupe_id = str(row[3])
    cur_items = row[4]
    if table == "zomato":
        lat_long = str(row[5])
    else:
        lat_long = str(row[6])
    return name,location,dedupe_id,cur_items,lat_long