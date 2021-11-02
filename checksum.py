"""Generate checksums for various lists"""
from hashlib import sha256
lists = ["antimalware.txt","Alternative list formats/antimalware_domains.txt","clickbait.txt","annoyances.txt"]
checksums = {}
for listi in lists:
  checksums[listi] = sha256(open(listi,"rb").read()).hexdigest()

checksumf = open("checksums.txt","w")
for item in checksums:
  checksumf.write("{}: {}\n".format(item,checksums[item]))
checksumf.close()
