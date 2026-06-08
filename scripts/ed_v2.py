import json
import datetime
import requests

print("LOADING DATA")
try:
	entry_data = json.loads(open("entry_data.json", encoding="UTF-8").read())
except:
	print("FAILED TO LOAD DATA")
	entry_data = {}
print("LOADED DATA")

print("LOADING DOMAINS")
domain_list = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().replace("\r\n","\n").split("\n")
print("LOADED DOMAINS")
current_date = datetime.datetime.now().isoformat()
entry_data["last_updated"] = current_date

def get_last_commit() -> str:
	try:
		return requests.get("https://api.github.com/repos/iam-py-test/my_filters_001/commits").json()[0]['html_url']
	except Exception as err:
		print(err)
		return None

last_commit = get_last_commit()

for e in domain_list:
	if (e not in entry_data or type(entry_data[e]) == str) and e != "last_updated":
		entry_data[e] = {
			"first_seen": current_date,
			"last_seen": current_date,
			"removed": False,
			"removed_date": "",
			"ed_version": "v2",
			"readded": False,
			"origin_add": "",
			"readd": "",
			"times_died": 0,
			"last_commit": last_commit
		}


for e in entry_data:
	if e not in domain_list and e != "last_updated" and e != "":
		if entry_data[e]["removed"] == False:
			entry_data[e]["removed"] = True
			entry_data[e]["removed_date"] = current_date
			entry_data[e]['removed_commit'] = last_commit

entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()
