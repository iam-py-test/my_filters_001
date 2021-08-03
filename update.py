"""Auto-create the domains versions of porn.txt and antimalware.txt"""
alldomains = {}
allips = {}

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
  alldomains[file] = []
  allips[file] = []
  for line in lines:
    if len(line.split("$")[0].split(".")) > 2:
      if isipdomain(line.split("$")[0]) == True:
        iponly.write(line.split("$")[0] + "\n")
        try:
          allips[file].append(line.split("$")[0])
        except Exception as err:
          print("Error:{}".format(err))
        continue
    if line == '' or line.startswith("!") or line.startswith("||") or line == '[Adblock Plus 2.0]':
      continue
    if line.split("$")[0] not in donedomains:
      alt.write("{}\n".format(line.split("$")[0].lower()))
      donedomains.append(line.split("$")[0].lower())
      alldomains[file].append(line.split("$")[0].lower())
mkalt("antimalware.txt","antimalware_domains.txt")
mkalt("porn.txt","porn_domains.txt")
#mkalt("antitypo.txt","antitypo_domains.txt")

print(allips)
print(alldomains)

def mkhosts(file,altname):
  donedomains = []
  List = open(file).read().split("\n")
  altfile = open(altname,"w")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  for line in List:
    if line.startswith("!"):
      altfile.write(line.replace("!","#"))
    elif line == "" or line.startswith("||") or line.startswith("[Adblock Plus 2.0]"):
      continue
    elif "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if isip == True:
        altfile.write("#IP address: {}".format(domain))
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("127.0.0.1 {}".format(domain))
        donedomains.append(domain)
    altfile.write("\n")

mkhosts("antimalware.txt","Alternative list formats/antimalware_hosts.txt")


def mkagh(file,altname):
  donedomains = []
  List = open(file).read().split("\n")
  altfile = open(altname,"w")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  for line in List:
    if line.startswith("!"):
      altfile.write(line)
    elif line == "" or line.startswith("||") or line.startswith("[Adblock Plus 2.0]"):
      continue
    elif "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if isip == True:
        altfile.write("{}".format(domain))
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("||{}^".format(domain))
        donedomains.append(domain)
    altfile.write("\n")

try:
  mkagh("antimalware.txt","Alternative list formats/antimalware_adguard_home.txt")
except:
  print("Error")
def mkabp(file,altname):
  donedomains = []
  List = open(file).read().split("\n")
  altfile = open(altname,"w")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  for line in List:
    if line.startswith("!"):
      altfile.write(line)
    if line.startswith("||"):
      altfile.write(line.split("$")[0][2:]
    elif line == "" or line.startswith("||") or line.startswith("[Adblock Plus 2.0]"):
      continue
    elif "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if isip == True:
        altfile.write("||{}^".format(domain))
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("||{}^".format(domain))
        donedomains.append(domain)
    altfile.write("\n")
                    
                    
try:
                    mkabp("antimalware.txt","Alternative list formats/antimalware_abp.txt")
except:
                    print("ABP error")
