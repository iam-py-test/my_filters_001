# My filters
This is a repo where I upload my filters. <br/>
Feel free to use any and all of them (they are under no copyright) in [uBlock Origin](https://github.com/gorhill/uBlock) (recommended) or AdGuard. <br/>
Please report any issues you have and I will try to fix them; please note I may not reply within the day the issue is posted as I am often busy.<br>
<img src="https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/totalentries.svg" width='130' height="20"> <img src="https://img.shields.io/github/last-commit/iam-py-test/my_filters_001">
<br><br>**Note: I am currently on vacation, and therefore can not respond to issue reports**

## Filters in this repo

#### Actively maintained
- The malicious website blocklist (antimalware.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=2))
- Annoyances (annoyances.txt)
- Anti-Norton tracking list (anti-norton-tracking.txt)


#### Not actively maintained but don't require frequent updates
- The useless filter list (useless-list.txt)
- [My anti-facebook list](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/antifacebook.txt)
- [My Enhanced Protection list](https://github.com/iam-py-test/my_filters_001/blob/main/enhanced_protection.txt)

#### Not frequently updated but still receive occasional updates
- The clickbait blocklist (clickbait.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=4))
- Anti-typosquatting list (antitypo.txt)
- Anti redirectors list (anti-redirectors.txt)
- DuckDuckGo Clean up (duckduckgo-clean-up.txt)

#### Extension lists which add onto my existing lists
- [Google Safe Browsing reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/google-safe-browsing-reverse-engineered.txt)
- [Microsoft Smart Screen reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/microsoft-smart-screen-reverse-engineered.txt)

#### Updated rairly but still technically supported
- Pornography Blocklist (porn.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=1))
- Anti-cookie-consent and paywalls list (anti-cookie+sign up.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=3))
- My anti-rickroll list (anti-rickroll-list.txt)

#### Lists for testing syntax
- Everything in the _Sandbox_ folder
- test_filter.txt

#### Dead lists which are not even complete
- trojan_protection_list.txt
- Anti-overprompted Windows antivirus list (could not find enough instances of this that would not break legitimate websites)
- scams.txt (redundant, moved to antimalware.txt)
- anti-cookie+sign up_extention.txt (had one purpose - to work with my custom scriptlets - but the website it was intended to work for changed cookie values to quickly for it to work)

The filters in the _Alternative list formats_ folder are versions of some of the lists above for different software. These are auto-generated, and thus updates to them must be made to the original list or [the Python script](https://github.com/iam-py-test/my_filters_001/blob/main/update.py) which generates them.<br>
Everything elsewhere, like the _Personal_ folder, is either completaly forgotten by me, or is likely to break websites

## Other formats


#### Antimalware
- HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_hosts.txt
- Domains only - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_domains.txt
- AdBlock Plus format (_highly_ not recommended due to lack of needed features - including the ability to prevent the loading of a domain) - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_abp.txt
#### Clickbait blocklist
- AdBlock Plus format - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_abp.txt
- Domains only - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_domains.txt
#### Pornograhy Blocklist
- HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_hosts.txt
- AdBlock Plus format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_abp.txt
- Domains only (i.e. PiHole) - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_domains.txt
- Pure (no comments) HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_pure_hosts.txt


#### Notes
- The DuckDuckGo Clean Up list is auto-generated from duckduckgo-clean-up.template and the domains/ips versions of my antimalware list. Changes in PRs should be made to either of those
- Google Safe Browsing reverse engineered and Microsoft Smartscreen reverse engineered _are not_ intended as lists of known malware domains, instead they are lists of domains/urls which are blocked by those services in an attempt to understand them and provide some of their protection to users of other browsers
- All the up-to-date HOSTs versions use 0.0.0.0 instead of 127.0.0.1, as per [#87](https://github.com/iam-py-test/my_filters_001/issues/87)
