num = 0
lists = ["porn.txt","antimalware.txt","antitypo.txt","anti-redirectors.txt","anti-cookie+sign up.txt","anti-rickroll-list.txt"]
for list in lists:
  lines = open(list).read().split('\n')
  for line in lines:
    if line.startswith("!") != True and line != "":
      num += 1
      
allentries = """<svg height="20" width="130" xmlns="http://www.w3.org/2000/svg" version="1.1">
  <text x="0" y="15" fill="red">{} total entries</text>
</svg>"""
totalentries = open("totalentries.svg","w")
totalentries.write(allentries.format(num))
totalentries.close()
