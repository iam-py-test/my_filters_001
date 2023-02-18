"""Verify the syntax of my antimalware list and verify there are no legit domains in it"""
import requests
# invalid syntax
invalidsyntax = ["$$","$docment","$alll","^all","$docs","$scripted","$alls","$documentall","$allall","$all$all","$all.","$docments","$doc$doc","|*$","$documentP","$window","$document$document"]

legitdomains = gooddomains + hosting + social + urlshorteners + malshare + nsfw
bannedfilters = []

# download allowlisted domains from my personal allowlist
try:
  legitdomains = requests.get("https://raw.githubusercontent.com/iam-py-test/allowlist/main/allowlist.txt").text.split("\n")
  # strip out empty strings - https://stackoverflow.com/questions/19875595/removing-empty-elements-from-an-array-in-python#19875634
  legitdomains = list(filter(bool,legitdomains))
  bannedfilters += list(filter(bool,requests.get("https://raw.githubusercontent.com/iam-py-test/allowlist/main/filter.txt").text.split("\n")))
  print("Added!")
except:
  pass

# the main text
lines = open("antimalware.txt","r",encoding="UTF-8").read().split("\n")
# a list of invalid lines/good domains found
invalidlines = []
# log
log = ""
totalscanned = 0

for line in lines:
    if line in bannedfilters:
      invalidlines.append(line)
    if line.startswith("!"):
        continue
    try:
      domain = line.split("^$")[0][2:]
      if domain in legitdomains:
        invalidlines.append(line)
        print("False positive detected: WARNING")
      for syntax in invalidsyntax:
        if syntax in line:
          invalidlines.append(line)
      totalscanned += 1
    except:
      continue

with open("invalidlines.md","w") as f:
  f.write("## Lines detected by Lint (out of {})".format(totalscanned))
  for line in invalidlines:
    f.write("\n{}<br>".format(line))
  f.close()
