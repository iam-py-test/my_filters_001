"""Verify the syntax of my antimalware list and verify there are no legit domains in it"""
import requests, publicsuffixlist

# static vars
LEGIT_DOMAINS_URL = "https://raw.githubusercontent.com/iam-py-test/allowlist/main/allowlist.txt"
WILDCARD_URL = "https://raw.githubusercontent.com/iam-py-test/allowlist/main/wildcard.txt"
BANNED_FILTERS_URL = ""https://raw.githubusercontent.com/iam-py-test/allowlist/main/filter.txt""
REPORT_FILENAME = "invalidlines.md"
INPUT_FILENAME = "antimalware.txt"

# invalid syntax
invalidsyntax = ["$$","$docment","$alll","^all","$docs","$scripted","$alls","$documentall","$allall","$all$all","$all.","$docments","$doc$doc","|*$","$documentP","$window","$document$document","$documnt"]

bannedfilters = []

p = publicsuffixlist.PublicSuffixList()

# download allowlisted domains from my personal allowlist
try:
  legitdomains = requests.get(LEGIT_DOMAINS_URL).text.split("\n")
  # strip out empty strings - https://stackoverflow.com/questions/19875595/removing-empty-elements-from-an-array-in-python#19875634
  legitdomains = list(filter(bool,legitdomains))
  bannedfilters += list(filter(bool,requests.get(BANNED_FILTERS_URL).text.split("\n")))
  wildcard_allow = requests.get(WILDCARD_URL).text.split("\n")
  print("Added!")
except:
  pass

# the main text
lines = open(INPUT_FILENAME,"r",encoding="UTF-8").read().split("\n")
# a list of invalid lines/good domains found
invalidlines = []
# log
log = ""
totalscanned = 0

for line in lines:
    if line in bannedfilters:
      invalidlines.append(line)
      continue
    if line.startswith("!") or line == "":
        continue
    try:
      for syntax in invalidsyntax:
        if syntax in line:
          invalidlines.append(line)
          break
      domain = line.split("^$")[0][2:]
      if domain in legitdomains:
        invalidlines.append(line)
        print("False positive detected: WARNING")
      else:
        privatedomain = publicsuffixlist.privatesuffix(domain)
        if privatedomain in wildcard_allow:
          invalidlines.append(line)
      totalscanned += 1
    except:
      continue

with open(REPORT_FILENAME,"w",encoding="UTF-8") as f:
  f.write("## Lines detected by Lint (out of {})".format(totalscanned))
  for line in invalidlines:
    f.write("\n{}<br>".format(line))
  f.close()
