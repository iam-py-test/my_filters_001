import os
from publicsuffixlist import PublicSuffixList

psl = PublicSuffixList()

list1 = """
! Title: The malicious website blocklist (lite)
! Description: I released that a lot of the domains in my antimalware list used the same TLDs, and those TLDs had almost no legit content. 
! Expires: 1 day

! Main blocking rules
||gdn^$document
||win^$document
||bid^$document
||top^$document,domain=~corriente.top
||monster^$document
||ooo^$document
||loan^$document
||agency^$document
||download^$document
||cricket^$document

! Domain/url blocking rules
"""
blockedtlds = ["gdn","win","bid","top","monster","ooo","loan","agency","download","cricket"]

lines = open("antimalware.txt").read().split("\n")
for line in lines:
  if line.startswith("||"):
    list1 += line + "\n"
  if line.startswith("!") or line == "" or line.startswith("#"):
    continue
  else:
    try:
      tld = psl.publicsuffix(line.split("$")[0])
      if tld in blockedtlds:
        continue
      else:
        list1 += line + "\n"
endlist = open("Alternative list formats/antimalware_lite.txt","w")
endlist.write(list1)
endlist.close()
