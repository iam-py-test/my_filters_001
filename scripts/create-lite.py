import datetime
import requests
import publicsuffixlist
import re

BANNED_FILTERS_URL = "https://raw.githubusercontent.com/iam-py-test/allowlist/main/filter.txt"

psl = publicsuffixlist.PublicSuffixList()

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

list1 = """[Adblock Plus 2.0]
! Title: The malicious website blocklist (lite)
! Description: A lighter version of The malicious website blocklist, which has no comments, removes redundant entries (i.e. subdomains of already blocked domains) and has some extra protections against mistakes
! Homepage: https://github.com/iam-py-test/my_filters_001
! Issues url: https://github.com/iam-py-test/my_filters_001/issues
! GitLab issues url (not checked as often): https://gitlab.com/iam-py-test/my_filters_001/-/issues
! Script last updated: 2023-5-25
! Last updated: {}
! Expires: 1 day

""".format(datetime.datetime.now().strftime("%y-%m-%d"))
done_entries = []
bannedfilters = []
done_domains = []
all_domains = []
try:
  bannedfilters += list(filter(bool,requests.get(BANNED_FILTERS_URL).text.split("\n")))
except:
  pass

deaddomains = open("dead.mwbcheck.txt", encoding="UTF-8").read().split("\n")

parse = None
def parse(lines):
  global done_domains
  global done_entries
  global all_domains
  lcontents = ""
  for line in lines:
    if line.startswith("!#include "):
      try:
        path = line[10:]
        lcontents += parse(open(path, encoding="UTF-8").read().replace("\r\n", "\n").split("\n"))
      except Exception as err:
        print(err)
    if line in done_entries or line in bannedfilters or line == "" or line.startswith("!") or line.startswith("#") or "[Adblock Plus 2.0]" in line:
      continue
    if line.startswith("||") and "/" in line:
      lcontents += line + "\n"
      done_entries.append(line)
      continue
    else:
      try:
        domain = line.split("^")[0][2:]
        entryoptions = ""
        try:
          entryoptions = line.split("^")[1]
        except:
          pass
        if psl.is_public(domain):
          continue
        if domain in deaddomains:
          continue
        rootdomain = psl.privatesuffix(domain)
        if rootdomain in done_domains or domain in done_domains:
          continue
        else:
          lcontents += line + "\n"
          done_entries.append(line)
          done_domains.append(domain)
          if "/" not in line and isipdomain(domain) == False and "#" not in domain and "$" not in domain and domain.endswith(".") == False and "domain" not in entryoptions:
            all_domains.append(domain)
      except Exception as err:
        print(err)
        lcontents += line + "\n"
        done_entries.append(line)
  return lcontents

lines = open("antimalware.txt",encoding="UTF-8").read().split("\n")
list1 += parse(lines)
endlist = open("Alternative list formats/antimalware_lite.txt","w",encoding="UTF-8")
endlist.write(list1)
endlist.close()

endlist = open("Alternative list formats/antimalware_lite_domains.txt","w",encoding="UTF-8")
endlist.write("\n".join(all_domains))
endlist.close()
