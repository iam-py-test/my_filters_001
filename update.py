import os
lines = open("antimalware.txt").read().split("\n")
alt = open("Alternative list formats/antimalware_domains.txt","w")
for line in lines:
  if line.startswith("||") and "^" in line:
    domain = line.split("$")[0][2:-1]
    alt.write("{}\n".format(domain))
    continue
  if line == '' or line.startswith("!") or line.startswith("||"):
    continue
  alt.write("{}\n".format(line.split("$")[0]))
