import os, sys, json

domain_reasons = {
	"domains": {}
}

mwb_full = open("antimalware.txt", encoding="UTF-8").read().split("\n")
buffer = []

for line in mwb_full:
	if line == "":
		buffer = []
		continue
	if line.startswith("#") or line.startswith("!"):
		buffer.append(line[1:].strip())
	else:
		if "/" in line or "*" in line or "domain=" in line:
			continue
		# from update.py
		domain = ""
		if line.startswith("||") and line.endswith("^"):
			domain = line[2:-1]
		elif line.startswith("||") and line.endswith("$"):
			domain = line[2:-1]
		elif line.startswith("||") and "$" in line:
			domain = line.split("^")[0][2:]
		if domain.endswith(".") or domain == "":
			continue
		domain_reasons['domains'][domain] = {
			'comments': buffer
		}
		buffer = []

domain_reasons_out = open("domain_reasons.json", 'w', encoding="UTF-8")
domain_reasons_out.write(json.dumps(domain_reasons))
