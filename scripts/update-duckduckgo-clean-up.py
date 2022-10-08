try:
  from datetime import date
  currentdate = date.today()
except:
  import subprocess
  subprocess.run("pip3 install datetime",shell=True)
  from datetime import date
  currentdate = date.today()
template = open("duckduckgo-clean-up.template")
endfile = open("duckduckgo-clean-up.txt","w")
maldomains = open("Alternative list formats/antimalware_domains.txt").read().split("\n")
malips = open("Alternative list formats/antimalware_ips.txt").read().split("\n")
maldomains.extend(malips)
total = ''
for line in maldomains:
  if line == '' or line.startswith("!"):
    continue
  total += """duckduckgo.com,3g2upl4pq6kufc4m.onion,duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion##[data-nrn="result"]:has(a[href*="://{}"])\nduckduckgo.com,3g2upl4pq6kufc4m.onion,duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion##.result:has(a[href*="://{}"])\n""".format(line,line)
endfile.write(template.read().replace("{{auto-gen-time}}",currentdate.strftime('%d/%m/%Y')).replace("{mal}",total))
endfile.close()
