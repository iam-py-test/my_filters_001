# My filters
This is a repo where I upload my filters. <br/>
Feel free to use any and all of them (they are under no copyright) in [uBlock Origin](https://github.com/gorhill/uBlock) (recommended) or AdGuard. <br/>
Please report any issues you have and I will try to fix them; please note I may not reply within the day the issue is posted as I am often busy.<br>
Thanks to all the people in https://github.com/iam-py-test/my_filters_001/blob/main/CONTRIBUTORS.md <br>

### Some stats: 
<a href="https://github.com/iam-py-test/my_filters_001/blob/main/stats.md"><img src="https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/totalentries.svg" width='130' height="20"></a><img src="https://img.shields.io/github/last-commit/iam-py-test/my_filters_001"> [![Update the alt lists](https://github.com/iam-py-test/my_filters_001/actions/workflows/test_commiter.yml/badge.svg)](https://github.com/iam-py-test/my_filters_001/actions/workflows/test_commiter.yml)

## Filters in this repo

#### Actively maintained
- The malicious website blocklist (antimalware.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=2))
- Annoyances (annoyances.txt)
- DuckDuckGo Clean up (duckduckgo-clean-up.txt)

#### Not actively maintained but don't require frequent updates
- [My anti-facebook list](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/antifacebook.txt)
- [My Enhanced Protection list](https://github.com/iam-py-test/my_filters_001/blob/main/enhanced_protection.txt)
- Anti-Norton tracking list (anti-norton-tracking.txt)


#### Not frequently updated but still receive occasional updates
- The clickbait blocklist (clickbait.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=4))
- Anti-typosquatting list (antitypo.txt)
- Anti redirectors list (anti-redirectors.txt)
- The cleaner Tor list (cleaner-tor.txt)
- The device privacy list (device_privacy.txt)


#### Extension lists which add onto my existing lists
- [Google Safe Browsing reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/google-safe-browsing-reverse-engineered.txt)
- [Microsoft Smart Screen reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/microsoft-smart-screen-reverse-engineered.txt)
- [The malicious website blocklist - uBlock Origin extension](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/anti-malware-ubo-extension.txt)

#### Updated rairly but still technically supported
- Pornography Blocklist (porn.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=1))
- Anti-cookie-consent and paywalls list (anti-cookie+sign up.txt) ([Subscribe](https://iam-py-test.github.io/add_list.html?id=3))
- My anti-rickroll list (anti-rickroll-list.txt)

#### Lists for testing syntax
- Everything in the _Sandbox_ folder
- The useless filter list (useless-list.txt)
- test_filter.txt

#### Dead lists which are not even complete
- trojan_protection_list.txt
- Anti-overpromoted Windows antivirus list (could not find enough instances of this that would not break legitimate websites)
- scams.txt (redundant, moved to antimalware.txt)
- anti-cookie+sign up_extention.txt (had one purpose - to work with my custom scriptlets - but the website it was intended to work for changed cookie values to quickly for it to work)

<br>The filters in the _Alternative list formats_ folder are versions of some of the lists above for different software. These are auto-generated, and thus updates to them must be made to the original list or [the Python script](https://github.com/iam-py-test/my_filters_001/blob/main/update.py) which generates them.<br>
Everything not listed above, like the filters in the _Personal_ folder, is either completely forgotten by me, or is likely to break websites due to its purpose or lack of regulation. <br>

**Need checksums for my lists? See checksums.txt for auto-generated SHA512 checksums**

## Other formats

#### The malicious website blocklist
- HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_hosts.txt
- Domains only - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_domains.txt
- AdBlock Plus format (not recommended) - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/antimalware_abp.txt
#### Clickbait blocklist
- AdBlock Plus format - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_abp.txt
- Domains only - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_domains.txt
#### Pornograhy Blocklist
- HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_hosts.txt
- AdBlock Plus format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_abp.txt
- Domains only (i.e. PiHole) - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_domains.txt
- Pure (no comments) HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_pure_hosts.txt

## Projects which use my lists (to my knowlage) 
- [Zelo72's Threat intelligence feeds](https://github.com/Zelo72/rpi) use the domains, HOSTS, and AdGuard versions of my antimalware and anti-clickbait lists
- [pallebone's PersonalPiholeListsPAllebone](https://github.com/pallebone/PersonalPiholeListsPAllebone) uses the domains version of my antimalware list
- [eded333's TheF\*ckingList](https://github.com/eded333/TheFuckingList) uses the uBlock Origin version of my antimalware list and the Anti-Norton Tracking list


#### Notes
- The DuckDuckGo Clean Up list is auto-generated from duckduckgo-clean-up.template and the domains/ips versions of my antimalware list. Changes in PRs should be made to either of those
- Google Safe Browsing reverse engineered and Microsoft Smartscreen reverse engineered _are not_ intended as lists of known malware domains, instead they are lists of domains/urls which are blocked by those services in an attempt to understand them and provide some of their protection to users of other browsers
- All the up-to-date HOSTs versions use 0.0.0.0 instead of 127.0.0.1, as per [#87](https://github.com/iam-py-test/my_filters_001/issues/87)
- The _domains_lite_ and _hosts_lite_ versions are unmaintained, however, the antimalware_lite is not
- If you are trying to use Tor to investigate an issue, try looking at [tor-relays-with-issues.md](https://github.com/iam-py-test/my_filters_001/blob/main/wiki/tor-relays-with-issues.md) for a list of Tor exits which are known to cause issues or which malware/scam domains block
- While the _Google Safe Browsing reverse engineered_ and _Microsoft Smartscreen reverse engineered_ lists can be installed on their own in uBlock Origin, _The malicious website blocklist - uBlock Origin extension_ can not as it is designed only to be included in _The malicious website blocklist_
