"""Automatically create other formats of my lists"""
import json
import sys, os
import re
import idna

ALT_FORMATS_LOC = "Alternative list formats"

alldomains = {}
allips = {}
reddomains = []
allentries = {}

# https://www.geeksforgeeks.org/how-to-validate-an-ip-address-using-regex/
is_ip_v4 = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
is_ip_v6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"
is_ip_v4_reg = re.compile(is_ip_v4)
is_ip_v6_reg = re.compile(is_ip_v6)

def isipdomain(domain):
  if re.search(is_ip_v4_reg,domain):
    return True
  if re.search(is_ip_v6_reg,domain):
    return True
  return False

def safe_encode(data):
  try:
    return idna.encode(data, uts46=True, transitional=True).decode()
  except Exception as err:
    print(err)
    return "" # temp fix for https://github.com/iam-py-test/my_filters_001/issues/116

def mkalt(file,alt):
  lines = open(file,encoding="UTF-8").read().split("\n")
  alt = open(f"{ALT_FORMATS_LOC}/{alt}","w",encoding="UTF-8")
  iponly = open("Alternative list formats/{}_ips.txt".format(file.split(".")[0]),"w",encoding="UTF-8")
  donedomains = []
  alldomains[file] = []
  allips[file] = []
  allentries[file] = []
  for line in lines:
    if line == '' or line.startswith("!") or line == '[Adblock Plus 2.0]' or "#" in line or "domain=" in line:
      continue
    domain = ""
    if "/" in line or "*" in line or "domain=" in line:
      continue
    if line.startswith("||") and line.endswith("^"):
      domain = line[2:-1]
    elif line.startswith("||") and line.endswith("$"):
      domain = line[2:-1]
      if domain.endswith(".") or domain == "":
        continue
    elif line.startswith("||") and "$" in line:
      domain = line.split("^")[0][2:]
      if domain.endswith(".") or domain == "":
        continue
    if isipdomain(domain) == True:
      iponly.write(domain + "\n")
      try:
        allips[file].append(domain)
        allentries[file].append(domain)
      except Exception as err:
        print("Error: {}".format(err))
      continue
    if line.startswith("||") and "/" not in line and "^" in line:
      try:
        try:
          domain = safe_encode(domain.lower())
        except:
          pass
        if domain == "":
          continue
        alt.write("{}\n".format(domain))
        if domain in donedomains:
          reddomains.append(domain)
        donedomains.append(domain)
        alldomains[file].append(domain)
        allentries[file].append(domain)
        continue
      except Exception as err:
        print("error: ",err)

mkalt("antimalware.txt","antimalware_domains.txt")
mkalt("antipup.txt","antipup_domains.txt")
mkalt("antitypo.txt","antitypo_domains.txt")
mkalt("clickbait.txt","clickbait_domains.txt")
mkalt("anti-redirectors.txt","anti-redirectors_domains.txt")
mkalt("antidynamicdns.txt","antidynamicdns_domains.txt")
mkalt("anti-privacy-analytics.txt", "anti-privacy-analytics_domains.txt")

def mkhosts(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read().split("\n")
  altfile = open(altname,"w",encoding='UTF-8')
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
        domain = safe_encode(line.split("^")[0][2:].lower())
        if isipdomain(domain) != True and domain != "":
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
        pass
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
mkhosts("antidynamicdns.txt","Alternative list formats/antidynamicdns_hosts.txt")


def mkagh(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read().split("\n")
  altfile = open(altname,"w",encoding="UTF-8")
  for line in List:
    if line.startswith("!"):
      altfile.write("{}\n".format(line))
    elif line.startswith("[Adblock Plus 2.0]") or line == " ":
      continue
    elif "^" in line:
      if line.startswith("||") and "/" not in line and "^" in line:
        try:
          domain = line.split("^")[0][2:].lower()
          if isipdomain(domain):
            altfile.write("{}\n".format(domain))
          else:
            altfile.write("||{}^\n".format(domain))
          donedomains.append(domain)
          continue
        except Exception as err:
          print(err)
      domain = line.split("^")[0].lower()
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
      elif line.startswith("||") and line.endswith("^"):
        endlist += line + "\n"
      elif line.startswith("||") and "$" in line:
        modifier = line.split("$")[1]
        if "all" in modifier or "doc" in modifier or "important" in modifier or "redirect" in modifier:
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

convert_to_sabp = None
def convert_to_sabp(clist,clistpath="./list.txt",include=False):
  """convert a list into ||domain^ syntax, removing IPs"""
  endlist = ""
  listlines = clist.split("\n")
  for line in listlines:
    try:
      if line.startswith("!") and line.startswith("!#") == False:
        continue
      elif line.startswith("||") and line.endswith("^") and "/" not in line:
        domain = safe_encode(line[2:-1])
        if isipdomain(domain) == False and domain != "":
          endlist += "||{}^\n".format(domain)
      elif line.startswith("||") and "$" in line and "/" not in line:
        domain = safe_encode(line.split("$")[0][2:-1])
        if isipdomain(domain) == False and domain != "":
          endlist += "||{}^\n".format(domain)
      elif line.startswith("!#include "):
        try:
          incpath = os.path.abspath(line[10:])
          inccontents = open(incpath, encoding="UTF-8").read().replace("! Title","! Included title")
          endlist += "{}\n".format(convert_to_sabp(inccontents,include=True))
        except:
          pass
      elif line.startswith("[Adblock") and include == False:
        pass
    except Exception as err:
      print(err,line)
  return endlist

def mksabp(file,altname):
  donedomains = []
  List = open(file,encoding="UTF-8").read()
  altfile = open(altname,"w",encoding="UTF-8")
  altfile.write(convert_to_sabp(List,clistpath=file))
  altfile.close()               
                    
try:
  mksabp("antimalware.txt","Alternative list formats/antimalware_abp_domainsonly.txt")
except Exception as err:
  print(err)

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
def adguardparse(data,lpath="./list.txt"):
  List = data.split("\n")
  endlist = ""
  for line in List:
    if line == "":
      endlist += "\n"
    elif line.startswith("!#include"):
        try:
            includepath = os.path.join(os.path.split(lpath)[0]," ".join(line.split(" ")[1:]))
            includecontent = open(includepath, encoding="UTF-8").read()
            endlist += adguardparse(includecontent,includepath)
        except Exception as err:
          print(err)
    elif line.startswith("!"):
      endlist += "{}\n".format(line)
    elif "[Adblock Plus 2.0]" in line:
      endlist += "{}\n".format(line)
    elif line.startswith("||") and "$" in line:
        endlist += "{}\n".format(line)
    elif line.startswith("||") and line.endswith("^"):
      endlist += "{}\n".format(line)
  return endlist

def mkadguard(file,altname):
  donedomains = []
  List = open(file, encoding="UTF-8").read()
  altfile = open(altname,"w",encoding="UTF-8")
  def isipdomain(domain):
    try:
      return domain in allips[file]
    except:
      pass
    return False
  altfile.write(adguardparse(List,file))
  altfile.close()
  
  
try:
  mkadguard("antimalware.txt","Alternative list formats/antimalware_adguard_app.txt")
except:
  print("AdGuard error")

def mkdnsmasq(file,altname):
  altfile = open(altname,"w", encoding="UTF-8")
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
  with open(altname,"w", encoding="UTF-8") as f:
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
  outf.write("""Write-Host \"PowerShell script for blocking malicious IPs in Windows Firewall"
Write-Host "Created by iam-py-test"
Write-Host "This must be run as admin and on Microsoft Windows 10/11 or else it will not work!"

Write-Host "Removing old rules"
Get-NetFirewallRule -DisplayName "iam-py-test - Block outbound connections to this ip" | Remove-NetFirewallRule
Get-NetFirewallRule -DisplayName "iam-py-test - Block inbound connections from this ip" | Remove-NetFirewallRule

Write-Host "Adding new rules"
""")
  for ip in ips:
    # safety check to make sure this doesn't turn into a prefect RCE
    if "\"" not in ip and ";" not in ip and "-" not in ip and ":/" not in ip:
      outf.write("New-NetFirewallRule -DisplayName \"iam-py-test - Block outbound connections to this ip\" -Direction outbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\nNew-NetFirewallRule -DisplayName \"iam-py-test - Block inbound connections from this ip\" -Direction Inbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\n".format(ip,ip))
  outf.write("\n\nWrite-Host \"All rules should have been added to the Windows Firewall\"\npause\n")
  outf.close()
try:
  mkps_firewall_block("antimalware.txt","Alternative list formats/antimalware_firewall_script.ps1")
except Exception as err:
  print(err)

def mkps_firewall_block_combined_rules(file,outfile):
  ips = allips[file]
  csi = ",".join(ips)
  print(ips[0])
  print(ips[1])
  outf = open(outfile,'w')
  outf.write("""Write-Host \"PowerShell script for blocking malicious IPs in Windows Firewall"
Write-Host "Created by iam-py-test"
Write-Host "This must be run as admin and on Microsoft Windows 10/11 or else it will not work!"

Write-Host "Removing old rules"
Get-NetFirewallRule -DisplayName "iam-py-test - Block outbound connections to this ip" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
Get-NetFirewallRule -DisplayName "iam-py-test - Block inbound connections from this ip" -ErrorAction SilentlyContinue | Remove-NetFirewallRule

Write-Host "Adding new rules"
""")
  outf.write("New-NetFirewallRule -DisplayName \"iam-py-test - Block outbound connections to this ip\" -Direction outbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\nNew-NetFirewallRule -DisplayName \"iam-py-test - Block inbound connections from this ip\" -Direction Inbound -LocalPort Any -Protocol tcp -Action Block -RemoteAddress {}\n".format(csi,csi))
  outf.write("\n\nWrite-Host \"All rules should have been added to the Windows Firewall\"\npause\n")
  outf.close()
try:
  mkps_firewall_block_combined_rules("antimalware.txt","Alternative list formats/antimalware_firewall_script_c.ps1")
except Exception as err:
  print(err)

def mkpac(file, outfile):
  # PAC file format copied from https://pgl.yoyo.org/adservers/serverlist.php?hostformat=proxyautoconfig&showintro=1&mimetype=plaintext
  # which is under MCRAE GENERAL PUBLIC LICENSE (version 4.r53)
  # see also https://github.com/hagezi/dns-blocklists/issues/1423
  pall_domains = alldomains[file]
  end_domains = []
  for d in pall_domains:
    end_domains.append(f"		  shExpMatch(host, \"{d}\")")
  pac_format = """function FindProxyForURL(url, host) {
   if (
[[LIST]]) {
       return "PROXY 127.0.0.1";
       }
   else {
       return "DIRECT";
       }
   }
""".replace("[[LIST]]", " ||\n".join(end_domains))
  outhandle = open(outfile, 'w', encoding="UTF-8")
  outhandle.write(pac_format)
  outhandle.close()
try:
  mkpac("antimalware.txt","Alternative list formats/antimalware.pac")
except Exception as err:
  print(err)

redd = open("reddomains.txt","w")
for domain in reddomains:
  redd.write("{}\n".format(domain))
redd.close()
