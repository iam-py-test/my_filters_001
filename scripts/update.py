"""Automatically create other formats of my lists"""
import json
import sys,os
import re
import idna

alldomains = {}
allips = {}
reddomains = []
allentries = {}

# https://www.geeksforgeeks.org/how-to-validate-an-ip-address-using-regex/
is_ip_v4 = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
is_ip_v6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"
is_ip_v4_reg = re.compile(is_ip_v4)
is_ip_v6_reg = re.compile(is_ip_v6)

def mkalt(file,alt):
  lines = open(file,encoding="UTF-8").read().split("\n")
  alt = open("Alternative list formats/{}".format(alt),"w",encoding="UTF-8")
  iponly = open("Alternative list formats/{}_ips.txt".format(file.split(".")[0]),"w",encoding="UTF-8")
  donedomains = []
  def isipdomain(domain):
    if re.search(is_ip_v4_reg,domain):
      return True
    if re.search(is_ip_v6_reg,domain):
      return True
    return False
  alldomains[file] = []
  allips[file] = []
  allentries[file] = []
  for line in lines:
    if line == '' or line.startswith("!") or line == '[Adblock Plus 2.0]' or "#" in line or "domain=" in line:
      continue
    if isipdomain(line.split("^$")[0][2:]) == True:
      iponly.write(line.split("^$")[0][2:] + "\n")
      try:
        allips[file].append(line.split("^$")[0][2:])
        allentries[file].append(line.split("^$")[0][2:])
      except Exception as err:
        print("Error: {}".format(err))
      continue
    if line.startswith("||") and "/" not in line and "^" in line:
      try:
        try:
          domain = idna.encode(line.split("^$")[0][2:].lower()).decode()
        except:
          domain = line.split("^$")[0][2:].lower()
        alt.write("{}\n".format(domain))
        if domain in donedomains:
          reddomains.append(line.split("$")[0])
        donedomains.append(domain)
        alldomains[file].append(domain)
        allentries[file].append(domain)
        continue
      except Exception as err:
        print("error: ",err)
    elif "/" in line and "|" in line:
      continue

mkalt("antimalware.txt","antimalware_domains.txt")
mkalt("antipup.txt","antipup_domains.txt")
mkalt("antitypo.txt","antitypo_domains.txt")
mkalt("clickbait.txt","clickbait_domains.txt")
mkalt("anti-redirectors.txt","anti-redirectors_domains.txt")

def mkhosts(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read().split("\n")
  altfile = open(altname,"w",encoding='UTF-8')
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
    if line == "# Note: This list includes a version of VXVault.net's malware distribution url list, formatted for adblockers, which is at https://github.com/iam-py-test/vxvault_filter":
      continue
    if line.startswith("!"):
      altfile.write("#" + line[1:])
    elif line.startswith("||") and "/" not in line and "^" in line:
      try:
        domain = idna.encode(line.split("^$")[0][2:].lower()).decode()
        if isipdomain(domain) != True:
          altfile.write("0.0.0.0 {}\n".format(domain))
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
  altfile.close()

mkhosts("antimalware.txt","Alternative list formats/antimalware_hosts.txt")
mkhosts("antitypo.txt","Alternative list formats/antitypo_hosts.txt")
mkhosts("anti-redirectors.txt","Alternative list formats/anti-redirectors_hosts.txt")

def mkagh(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read().split("\n")
  altfile = open(altname,"w",encoding="UTF-8")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  for line in List:
    if line.startswith("!"):
      altfile.write("{}\n".format(line))
    elif line.startswith("[Adblock Plus 2.0]") or line == " ":
      continue
    elif "$" in line:
      if line.startswith("||") and "/" not in line and "^" in line:
        try:
          domain = line.split("^$")[0][2:].lower()
          if isipdomain(domain):
            altfile.write("{}\n".format(domain))
          else:
            altfile.write("||{}^\n".format(domain))
          donedomains.append(domain)
          continue
        except Exception as err:
          print(err)
      domain = line.split("$")[0].lower()
      if domain in donedomains:
        continue
      if domain != "" and domain not in donedomains and "/" not in domain:
        if isipdomain(domain):
          altfile.write("{}\n".format(domain))
        else:
          altfile.write("||{}^\n".format(domain))
        donedomains.append(domain)
    elif line == "" or line == "\n":
      altfile.write("\n")

try:
  mkagh("antimalware.txt","Alternative list formats/antimalware_adguard_home.txt")
except:
  print("Error")

convert_to_abp = None
def convert_to_abp(clist,clistpath="./list.txt",include=False):
  endlist = ""
  listlines = clist.split("\n")
  for line in listlines:
    try:
      if line.startswith("!") and line.startswith("!#") == False:
        endlist += "{}\n".format(line)
      elif line.startswith("||") and "$" in line:
        modifier = line.split("$")[1]
        if "all" in modifier or "doc" in modifier or "important" in modifier:
          modifier = ""
        else:
          modifier = "${}".format(modifier)
        endlist += "{}{}\n".format(line.split("$")[0],modifier)
      elif line.startswith("!#include "):
        try:
          incpath = os.path.abspath(line[10:])
          inccontents = open(incpath,encoding="UTF-8").read().replace("! Title","! Included title")
          endlist += "{}\n".format(convert_to_abp(inccontents,include=True))
        except:
          pass
      elif line.startswith("||"):
        endlist += "{}\n".format(line)
      elif "##" in line and "+js" not in line and ":remove" not in line and "##^" not in line:
        endlist += "{}\n".format(line)
      elif line == "":
        endlist += "\n"
      elif line.startswith("[Adblock") and include == False:
        endlist += line + "\n"
    except Exception as err:
      print(err,line)
  return endlist 


def mkabp(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read()
  altfile = open(altname,"w",encoding="UTF-8")
  altfile.write(convert_to_abp(List,clistpath=file))
  altfile.close()               
                    
try:
  mkabp("antimalware.txt","Alternative list formats/antimalware_abp.txt")
  mkabp("clickbait.txt","Alternative list formats/clickbait_abp.txt")
except Exception as err:
  print("ABP error: {}".format(err))
def mkpurehosts(file,altname):
  altfile = open(altname,"w")
  for domain in alldomains[file]:
      altfile.write("0.0.0.0 {}\n".format(domain))
  altfile.close()
try:
  mkpurehosts("antimalware.txt","Alternative list formats/antimalware_pure_hosts.txt")
except:
  print("Pure hosts error")

adguardparse = None # this is a really bad solution to allow a function to use it's self
def adguardparse(data):
  List = data.split("\n")
  endlist = ""
  for line in List:
    if line == "":
      endlist += "\n"
    elif line.startswith("!#include"):
        try:
            includecontent = open(" ".join(line.split(" ")[1:])).read()
            endlist += adguardparse(includecontent)
        except Exception as err:
          print(err)
    elif line.startswith("!"):
      endlist += "{}\n".format(line)
    elif "[Adblock Plus 2.0]" in line:
      endlist += "{}\n".format(line)
    elif line.startswith("||") and "$" in line:
        endlist += "{}\n".format(line)
  return endlist

def mkadguard(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read()
  altfile = open(altname,"w",encoding="UTF-8")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  altfile.write(adguardparse(List))
  altfile.close()
  
  
try:
  mkadguard("antimalware.txt","Alternative list formats/antimalware_adguard_app.txt")
except:
  print("AdGuard error")

def mkdnsmasq(file,altname):
  altfile = open(altname,"w",encoding="UTF-8")
  for domain in alldomains[file]:
    if domain == "" or "|" in domain:
      continue
    altfile.write("address=/{}/\n".format(domain))
  altfile.close()
try:
  mkdnsmasq("antimalware.txt","Alternative list formats/antimalware_dnsmasq.txt")
except Exception as err:
  print(err)

def mkJSON(file,altname):
  all = json.dumps(allentries[file])
  with open(altname,"w") as f:
    f.write(all)
    f.close()

try:
  mkJSON("antimalware.txt","Alternative list formats/antimalware_json.json")
except Exception as err:
  print(err)

def mkps_firewall_block(file,outfile):
  ips = allips[file]
  print(ips[0])
  print(ips[1])
  outf = open(outfile,'w')
  outf.write("echo \"PowerShell script for blocking malicious IPs in Windows Firewall\"\n")
  outf.write("echo \"Created by iam-py-test\"\n")
  outf.write("echo \"This must be run as admin and on Microsoft Windows 10/11 or else it will not work!\"\n\n")
  for ip in ips:
    # safety check to make sure this doesn't turn into a prefect RCE
    if "\"" not in ip and ";" not in ip and "-" not in ip and ":/" not in ip:
      outf.write("New-NetFirewallRule -DisplayName \"iam-py-test - Block outbound connections to this ip\" -Direction outbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\nNew-NetFirewallRule -DisplayName \"iam-py-test - Block inbound connections from this ip\" -Direction Inbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\n".format(ip,ip))
  outf.write("\n\necho \"All rules should have been added to the Windows Firewall\"\npause\n")
  outf.close()
#try:
#  mkps_firewall_block("antimalware.txt","Alternative list formats/antimalware_firewall_script.ps1")
#except Exception as err:
#  print(err)

redd = open("reddomains.txt","w")
for domain in reddomains:
  redd.write("{}\n".format(domain))
redd.close()
