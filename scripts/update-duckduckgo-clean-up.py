from datetime import date
currentdate = date.today()

FILTER_TEMPLATE = "duckduckgo.com,duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion##[data-nrn=\"result\"]:has(a[href*=\"://{}\"])\nduckduckgo.com,duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion##.result:has(a[href*=\"://{}\"])\n"
ALT_FOLDER = "Alternative list formats"
ALT_AM_DOMAINS = f"{ALT_FOLDER}/antimalware_domains.txt"
ALT_AM_IPS = f"{ALT_FOLDER}/antimalware_ips.txt"
ALT_PUP_DOMAINS = f"{ALT_FOLDER}/antipup_domains.txt"
ALT_PUP_IPS = f"{ALT_FOLDER}/antipup_ips.txt"
TEMPLATE_FILE = "duckduckgo-clean-up.template"
OUTPUT_FILE = "duckduckgo-clean-up.txt"
current_date = currentdate.strftime('%d/%m/%Y')

template = open(TEMPLATE_FILE)
endfile = open(OUTPUT_FILE,"w")
maldomains_file = open(ALT_AM_DOMAINS)
maldomains = maldomains_file.read().split("\n")
malips_file = open(ALT_AM_IPS)
malips = malips_file.read().split("\n")
pupdomains_file = open(ALT_PUP_DOMAINS)
pupdomains = pupdomains_file.read().split("\n")
pupips_file = open(ALT_PUP_IPS)
pupips = pupips_file.read().split("\n")
maldomains += malips
pupdomains += pupips
total = ''
totalpups = ''
for line in maldomains:
  if line == '' or line.startswith("!"):
    continue
  total += FILTER_TEMPLATE.format(line,line)
for line in pupdomains:
  if line == '' or line.startswith("!"):
    continue
  totalpups += FILTER_TEMPLATE.format(line,line)

endfile.write(template.read().replace("{{auto-gen-time}}",current_date).replace("{mal}",total).replace("{pup}",totalpups))
# close all files
endfile.close()
template.close()
maldomains_file.close()
malips_file.close()
pupdomains_file.close()
pupips_file.close()
