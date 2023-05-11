from datetime import date
currentdate = date.today().strftime('%d/%m/%Y')

FILTER_LINE = "search.brave.com##div.fdb.snippet:has(a[href*=\"://{}\"])\n"
TEMPLATE_FILENAME = "brave-clean-up.template"

template = open(TEMPLATE_FILENAME)
endfile = open("brave-clean-up.txt","w",encoding="UTF-8")
maldomains = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().split("\n")
malips = open("Alternative list formats/antimalware_ips.txt", encoding="UTF-8").read().split("\n")
pupdomains = open("Alternative list formats/antipup_domains.txt", encoding="UTF-8").read().split("\n")
pupips = open("Alternative list formats/antipup_ips.txt", encoding="UTF-8").read().split("\n")
maldomains.extend(malips)
pupdomains.extend(pupips)
total = ''
totalpups = ''
for line in maldomains:
  if line == '' or line.startswith("!"):
    continue
  total += FILTER_LINE.format(line)
for line in pupdomains:
  if line == '' or line.startswith("!"):
    continue
  totalpups += FILTER_LINE.format(line)

endfile.write(template.read().replace("{{auto-gen-time}}",currentdate).replace("{mal}",total).replace("{pup}",totalpups))
endfile.close()
template.close()
