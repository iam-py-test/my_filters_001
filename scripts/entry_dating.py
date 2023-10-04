import os, sys, json, datetime, socket, random

def is_alive(domain):
    try:
        return socket.gethostbyname(domain) != "0.0.0.0"
    except:
        return False

try:
    entry_data = json.loads(open("entry_data.json", encoding="UTF-8").read())
except:
    entry_data = {}

domain_list = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().replace("\r\n","\n").split("\n")
current_date = datetime.datetime.now().isoformat()
entry_data["last_updated"] = current_date

for e in domain_list:
    if e not in entry_data and e != "last_updated":
        entry_data[e] = {
            "first_seen": current_date,
            "last_seen": current_date,
            "removed": False,
            "removed_date": "",
            "last_checked": "",
            "check_counter": random.randint(0, 35),
            "check_status": None
        }
    else:
        entry_data[e]["last_seen"] = current_date
        entry_data[e]["removed"] = False
        entry_data[e]["removed_date"] = ""
        if "check_counter" not in entry_data[e]:
            entry_data[e]["check_counter"] = random.randint(0, 45)
        if "last_checked" not in entry_data[e]:
            entry_data[e]["last_checked"] = "Unknown"
        entry_data[e]["check_counter"] += 1
        if entry_data[e]["check_counter"] > 50:
            entry_data[e]["check_status"] = is_alive(e)
            entry_data[e]["last_checked"] = current_date
            entry_data[e]["check_counter"] = 0

for e in entry_data:
    if e not in domain_list and e != "last_updated":
        try:
            entry_data[e]["removed"] = True
            entry_data[e]["removed_date"] = current_date
        except Exception as err:
            print(err, e, entry_data[e])

entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()
