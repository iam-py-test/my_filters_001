try:
  from datetime import date
  currentdate = date.today()
except:
  import subprocess
  subprocess.run("pip3 install datetime",shell=True)
  from datetime import date
  currentdate = date.today()
template = open("brave-clean-up.template")
endfile = open("brave-clean-up.txt","w")
maldomains = open("Alternative list formats/antimalware_domains.txt").read().split("\n")
malips = open("Alternative list formats/antimalware_ips.txt").read().split("\n")
pupdomains = open("Alternative list formats/antipup_domains.txt").read().split("\n")
pupips = open("Alternative list formats/antipup_ips.txt").read().split("\n")
maldomains.extend(malips)
pupdomains.extend(pupips)
total = ''
totalpups = ''
for line in maldomains:
  if line == '' or line.startswith("!"):
    continue
  total += """search.brave.com##div.fdb.snippet:has(a[href*="://{}"])\n""".format(line)
for line in pupdomains:
  if line == '' or line.startswith("!"):
    continue
  totalpups += """search.brave.com##div.fdb.snippet:has(a[href*="://{}"])\n""".format(line)

endfile.write(template.read().replace("{{auto-gen-time}}",currentdate.strftime('%d/%m/%Y')).replace("{mal}",total).replace("{pup}",totalpups))
endfile.close()
