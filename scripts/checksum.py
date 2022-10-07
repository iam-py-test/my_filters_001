"""Generate checksums for various lists"""
from hashlib import sha256
import os
lists = ["antimalware.txt","clickbait.txt","annoyances.txt","porn.txt","antitypo.txt","anti-redirectors.txt","duckduckgo-clean-up.txt","special_lists/google-safe-browsing-reverse-engineered.txt","special_lists/anti-malware-ubo-extension.txt"]
checksums = {}
for listi in lists:
  checksums[listi] = sha256(open(listi,"rb").read()).hexdigest()
for root,dirs,files in os.walk("Alternative list formats"):
  for file in files:
    checksums[os.path.join(root,file)] = sha256(open(os.path.join(root,file),"rb").read()).hexdigest()

checksumf = open("checksums.txt","w")
for item in checksums:
  checksumf.write("{}: {}\n".format(item,checksums[item]))

checksumf.close()
