"""Generate checksums for various lists"""
from hashlib import sha256
import os
lists = ["antimalware.txt","clickbait.txt","annoyances.txt","antitypo.txt","anti-redirectors.txt","duckduckgo-clean-up.txt","special_lists/google-safe-browsing-reverse-engineered.txt","special_lists/anti-malware-ubo-extension.txt","Alternative list formats/antimalware_domains.txt","Alternative list formats/antimalware_hosts.txt","Alternative list formats/antimalware_abp.txt","Alternative list formats/antimalware_adguard_app.txt","Alternative list formats/antimalware_adguard_home.txt","Alternative list formats/antimalware_dnsmasq.txt","Alternative list formats/antimalware_ips.txt","Alternative list formats/antimalware_lite.txt","Alternative list formats/antimalware_pure_hosts.txt"]
checksums = {}
for listi in lists:
  checksums[listi] = sha256(open(listi,"rb").read()).hexdigest()

checksumf = open("checksums.txt","w")
for item in checksums:
  checksumf.write("{}: {}\n".format(item,checksums[item]))

checksumf.close()
