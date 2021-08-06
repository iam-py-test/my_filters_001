template = open("duckduckgo-clean-up.template")
endfile = open("duckduckgo-clean-up.txt","w")
maldomains = open("Alternative list formats/antimalware_domains.txt").read().split("\n")
malips = open("Alternative list formats/antimalware_ips.txt").read().split("\n")
maldomains.extend(malips)
total = ''
for line in maldomains:
  if line == '':
    continue
  total += """duckduckgo.com##.result:has(a[href*="{domain}"])
duckduckgo.com##.sitelink:has(a[href*="{domain}"])\n""".replace("{domain}",line)
endfile.write(template.read().replace("{mal}",total))
endfile.close()
