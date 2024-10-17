import os, sys, string

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source",help="Where the MWB is")
parser.add_argument("outdir",help="Where to save to")
args = parser.parse_args()

if os.path.exists(args.outdir) == False:
    print("Not found. Creating...")
    os.makedirs(args.outdir)

mwb_parts = {

}

mwb_file = open(args.source,encoding="UTF-8")
mwb = mwb_file.read().split("\n")
mwb_file.close()

part_name = ""
titlearea = ""

print(os.getcwd(), args)

include_list = None
def include_list(path,parentpath):
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
        mwb_parts[part_name] += l + "\n"

part_explain = """This folder includes each of the sections of The malicious website blocklist, so you can use only rules from specific sections (i.e. only block scams).
Sections:

"""

for part in mwb_parts:
    end_parts = []
    for line in mwb_parts[part].split("\n"):
        if line.startswith("~"):
            end_parts.append(line[1:])
        else:
            end_parts.append(line)
    mwb_parts[part] = "\n".join(end_parts)

for part in mwb_parts:
    partfilename = os.path.join(args.outdir,part)
    print(partfilename)
    partfile = open(partfilename,'w',encoding="UTF-8")
    partfile.write(titlearea)
    partfile.write(mwb_parts[part])
    partfile.close()
    part_explain += f"[{part}](./{part.replace(' ','%20')})<br>\n"

readme = open(os.path.join(args.outdir,"README.md"),'w')
readme.write(part_explain)
readme.close()
