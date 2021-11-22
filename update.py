"""Auto-create the domains versions of porn.txt and antimalware.txt"""
alldomains = {}
allips = {}
reddomains = []

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
    if len(line.split("^$")[0].split(".")) > 2:
      if isipdomain(line.split("^$")[0][2:]) == True:
        iponly.write(line.split("^$")[0][2:] + "\n")
        try:
          allips[file].append(line.split("^$")[0][2:])
        except Exception as err:
          print("Error:{}".format(err))
        continue
    if line.startswith("||") and "/" not in line and "^" in line:
      try:
        domain = line.split("^$")[0][2:].lower()
        alt.write("{}\n".format(domain))
        donedomains.append(domain)
        alldomains[file].append(domain)
        continue
      except:
        pass
    if line == '' or line.startswith("!") or line == '[Adblock Plus 2.0]':
      continue
    if line.split("$")[0] in donedomains:
      reddomains.append(line.split("$")[0])
    if line.split("$")[0] not in donedomains:
      alt.write("{}\n".format(line.split("$")[0].lower()))
      donedomains.append(line.split("$")[0].lower())
      alldomains[file].append(line.split("$")[0].lower())
mkalt("antimalware.txt","antimalware_domains.txt")
mkalt("porn.txt","porn_domains.txt")
mkalt("antitypo.txt","antitypo_domains.txt")
mkalt("clickbait.txt","clickbait_domains.txt")
mkalt("anti-redirectors.txt","anti-redirectors_domains.txt")

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
    if line.startswith("! Format notes:"):
      altfile.write('# Format notes: This format is designed for a system wide HOSTS file, and can also be used with tools that support this format. Not recommended for uBlock Origin or AdGuard\n')
      continue
    if line.startswith("!"):
      altfile.write("#" + line[1:])
    elif line.startswith("||") and "/" not in line and "^" in line:
      try:
        domain = line.split("^$")[0][2:].lower()
        if isipdomain(domain) != True:
          alt.write("{}\n".format(domain))
          donedomains.append(domain)
        continue
      except:
        pass
    elif line == "" or line.startswith("||") or line.startswith("[Adblock Plus 2.0]"):
      continue
    elif "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if isip == True:
        altfile.write("#IP address: {}".format(domain))
      if domain in donedomains:
        continue
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("0.0.0.0 {}".format(domain))
        donedomains.append(domain)
    altfile.write("\n")

mkhosts("antimalware.txt","Alternative list formats/antimalware_hosts.txt")
mkhosts("antitypo.txt","Alternative list formats/antitypo_hosts.txt")
mkhosts("porn.txt","Alternative list formats/porn_hosts.txt")
mkhosts("anti-redirectors.txt","Alternative list formats/anti-redirectors_hosts.txt")

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
    if line.startswith("! Format notes: "):
      altfile.write('! Format notes: This format is designed for AdGuard Home, and should not be used in AdGuard\n')
      continue
    if line.startswith("!"):
      altfile.write(line)
    elif line == "" or line.startswith("||") or line.startswith("[Adblock Plus 2.0]"):
      continue
    elif "$" in line:
      if line.startswith("||") and "/" not in line and "^" in line:
        try:
          domain = line.split("^$")[0][2:].lower()
          if isipdomain(domain):
            alt.write("{}\n".format(domain))
          else:
            alt.write("||{}^\n".format(domain))
          donedomains.append(domain)
          continue
        except:
          pass
      domain = line.split("$")[0].lower()
      if domain in donedomains:
        continue
      if domain != "" and domain not in donedomains:
        if isipdomain(domain):
          altfile.write("{}".format(domain))
        else:
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
    if line.startswith("! Format notes: "):
      altfile.write("! Format notes: This format is designed for use in AdBlock Plus. However, I recommend you do not use AdBlock Plus with this list, due to lack of support for full website blocking and some other more advanced features\n")
    if line.startswith("!"):
      altfile.write(line)
      altfile.write("\n")
      continue
    if line.startswith("||"):
      altfile.write(line.split("$")[0])
      altfile.write("\n")
      continue
    if "[Adblock Plus 2.0]" in line:
      altfile.write(line)
      
    if "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if domain in donedomains:
        continue
      if isip == True:
        altfile.write("||{}^".format(domain))
        donedomains.append(domain)
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("||{}^".format(domain))
        donedomains.append(domain)
    altfile.write("\n")
                    
                    
try:
                    mkabp("antimalware.txt","Alternative list formats/antimalware_abp.txt")
                    mkabp("porn.txt","Alternative list formats/porn_abp.txt")
                    mkabp("clickbait.txt","Alternative list formats/clickbait_abp.txt")
except:
                    print("ABP error")
def mkpurehosts(file,altname):
  altfile = open(altname,"w")
  for domain in alldomains[file]:
      altfile.write("0.0.0.0 {}\n".format(domain))
try:
  mkpurehosts("porn.txt","Alternative list formats/porn_pure_hosts.txt")
  mkpurehosts("antimalware.txt","Alternative list formats/antimalware_pure_hosts.txt")
except:
  print("Pure hosts error")

def mkadguard(file,altname):
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
    if line.startswith("! Format notes: "):
      altfile.write("! Format notes: This format is designed for use in AdGuard's desktop app\n")
      continue
    if line.startswith("!"):
      altfile.write(line)
      altfile.write("\n")
      continue
    if line.startswith("||"):
      altfile.write(line.split("$")[0])
      altfile.write("\n")
      continue
    if "[Adblock Plus 2.0]" in line:
      altfile.write(line)
      
    if "$" in line:
      domain = line.split("$")[0].lower()
      isip = isipdomain(domain)
      if isip == True:
        altfile.write("{}$network".format(domain))
      if isip == False and domain != "" and domain not in donedomains:
        altfile.write("||{}^".format(domain))
        donedomains.append(domain)
    altfile.write("\n")

  
try:
  mkadguard("antimalware.txt","Alternative list formats/antimalware_adguard_app.txt")
except:
  print("AdGuard error")

redd = open("reddomains.txt","w")
for domain in reddomains:
  redd.write("{}\n".format(domain))
redd.close()
