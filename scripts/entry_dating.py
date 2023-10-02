import os, sys, json, datetime

try:
    entry_data = json.loads(open("entry_data.json", encoding="UTF-8").read())
except:
    entry_data = {}

domain_list = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().replace("\r\n","\n").split("\n")
current_date = datetime.datetime.now().isoformat()
entry_data["last_updated"] = current_date

for e in domain_list:
    if e not in entry_data:
        entry_data[e] = {
            "first_seen": current_date,
            "last_seen": current_date
        }
    else:
        entry_data[e]["last_seen"] = current_date

entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()