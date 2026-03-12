"""
Code copied from mwb_parts.py
"""

import os, sys, string, re

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source",help="Where the MWB is")
parser.add_argument("outfile",help="Where to save to")
args = parser.parse_args()

mwb_parts = {

}

mwb_file = open(args.source,encoding="UTF-8")
mwb = mwb_file.read().split("\n")
mwb_file.close()

part_name = ""
titlearea = ""

# https://www.geeksforgeeks.org/how-to-validate-an-ip-address-using-regex/
is_ip_v4 = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
is_ip_v6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
			 "([0-9a-fA-F]){1,4}"
is_ip_v4_reg = re.compile(is_ip_v4)
is_ip_v6_reg = re.compile(is_ip_v6)

def isipdomain(domain: str) -> bool:
	if re.search(is_ip_v4_reg,domain):
		return True
	if re.search(is_ip_v6_reg,domain):
		return True
	return False

def extract_domain(line: str) -> str:
	ext_line = line
	if ext_line.startswith("||"):
		ext_line = ext_line[2:]
	if "/" in ext_line or "*" in ext_line or "$third-party" in ext_line or ",third-party" in ext_line:
		return "" # bad programming practice, I know
	if "$" in ext_line:
		ext_line = ext_line.split("$")[0]
	if ext_line.endswith("^"):
		ext_line = ext_line[:-1]
	return ext_line

include_list = None
def include_list(path: str, parentpath: str) -> str:
	reldir = os.path.split(parentpath)[0]
	includepath = os.path.join(reldir,path)
	try:
		includecontentfile = open(includepath,encoding="UTF-8")
		includefilecontent = includecontentfile.read()
		includefilecontentlines = includefilecontent.split("\n")
		includecontent = ""
		for l in includefilecontentlines:
			if l.startswith("!#include"):
				includecontent += include_list(l[10:],includepath)
			else:
				includecontent += l + "\n"
		includecontentfile.close()
		return includecontent + "\n"
	except Exception as err:
		print(err,includepath)
		return ""

for l in mwb:
	if l.startswith("~"):
		l = l[1:]
	if l.startswith("! ---- "):
		part_name = l[7:-5]
		if part_name.startswith(" "):
			part_name = part_name[1:]
		mwb_parts[part_name] = ""
	elif part_name == "":
		titlearea += l + "\n"
	elif l.startswith("!#include "):
		includepath = l[10:]
		mwb_parts[part_name] += include_list(includepath,args.source)
	else:
		ext_domain = extract_domain(l)
		if ext_domain != "" and "." in ext_domain:
			mwb_parts[part_name] += ext_domain + "\n"

for part in mwb_parts:
	if part == "PUPs":
		continue
	end_parts = []
	for line in mwb_parts[part].split("\n"):
		if line.startswith("~"):
			end_parts.append(line[1:])
		else:
			end_parts.append(line)
	mwb_parts[part] = "\n".join(end_parts)

outfile = open(args.outfile, 'w', encoding="UTF-8")
outfile.write(titlearea)

for part in mwb_parts:
	outfile.write(mwb_parts[part] + "\n")
outfile.close()

