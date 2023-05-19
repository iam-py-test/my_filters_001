import datetime
import requests
import publicsuffixlist

BANNED_FILTERS_URL = "https://raw.githubusercontent.com/iam-py-test/allowlist/main/filter.txt"

psl = publicsuffixlist.PublicSuffixList()

list1 = """[Adblock Plus 2.0]
! Title: The malicious website blocklist (lite)
! Description: A lighter version of The malicious website blocklist, which has no comments, removes redundant entries (i.e. subdomains of already blocked domains) and has some extra protections against mistakes
! Homepage: https://github.com/iam-py-test/my_filters_001
! Issues url: https://github.com/iam-py-test/my_filters_001/issues
! GitLab issues url (not checked as often): https://gitlab.com/iam-py-test/my_filters_001/-/issues
! Script last updated: 18/5/2023
! Last updated: {}
! Expires: 1 day

""".format(datetime.datetime.now().strftime("%d/%m/%y"))
done_entries = []
bannedfilters = []
done_domains = []
try:
  bannedfilters += list(filter(bool,requests.get(BANNED_FILTERS_URL).text.split("\n")))
except:
  pass


lines = open("antimalware.txt",encoding="UTF-8").read().split("\n")
for line in lines:
  if line in done_entries or line in bannedfilters:
    continue
  if line.startswith("||") and "/" in line:
    list1 += line + "\n"
    done_entries.append(line)
    continue
  if line.startswith("!") or line == "" or line.startswith("#") or "[Adblock Plus 2.0]" in line:
    continue
  else:
    try:
      domain = line.split("^")[0][2:]
      rootdomain = psl.privatesuffix(domain)
      if rootdomain in done_domains:
        continue
      else:
        list1 += line + "\n"
        done_entries.append(line)
        done_domains.append(domain)
    except Exception as err:
      print(err)
      list1 += line + "\n"
      done_entries.append(line)
endlist = open("Alternative list formats/antimalware_lite.txt","w",encoding="UTF-8")
endlist.write(list1)
endlist.close()
