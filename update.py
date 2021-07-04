"""Auto-create the domains versions of porn.txt and antimalware.txt"""
def mkalt(file,alt):
  lines = open(file).read().split("\n")
  alt = open("Alternative list formats/{}".format(alt),"w")
  iponly = open("Alternative list formats/{}_ips.txt".format(file.split(".")[0]),"w")
  donedomains = []
  def isipdomain(domain):
    try:
      import socket
      if socket.gethostbyname(domain) == domain:
        return True
    except:
      pass
    return False
  
  for line in lines:
    if isipdomain(line.split("$")[0]) == True:
      iponly.write(line.split("$")[0] + "\n")
      continue
    if line == '' or line.startswith("!") or line.startswith("||") or line == '[Adblock Plus 2.0]':
      continue
    if line.split("$")[0] not in donedomains:
      alt.write("{}\n".format(line.split("$")[0]))
      donedomains.append(line.split("$")[0].lower())
mkalt("antimalware.txt","antimalware_domains.txt")
mkalt("porn.txt","porn_domains.txt")
mkalt("antitypo.txt","antitypo_domains.txt")
