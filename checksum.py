"""Generate checksums for various lists"""
from hashlib import sha512
lists = ["antimalware.txt","Alternative list formats/antimalware_domains.txt","clickbait.txt","annoyances.txt","porn.txt","antitypo.txt","anti-redirectors.txt","duckduckgo-clean-up.txt","special_lists/google-safe-browsing-reverse-engineered.txt","special_lists/anti-malware-ubo-extension.txt"]
checksums = {}
for listi in lists:
  checksums[listi] = sha512(open(listi,"rb").read()).hexdigest()

checksumf = open("checksums.txt","w")
for item in checksums:special_lists/anti-malware-ubo-extension.txt
  checksumf.write("{}: {}\n".format(item,checksums[item]))
checksumf.close()
