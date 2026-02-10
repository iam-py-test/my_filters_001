# My filters
This is a collection of filterlists made by me (iam-py-test).<br>
Feel free to use any and all of them in [uBlock Origin](https://github.com/gorhill/uBlock), AdGuard, AdBlock Plus (special version required), or in any other way (i.e. PiHole, /etc/hosts) <br/>
Please report any issues you have and I will try to fix them; please note I may not reply within the day the issue is posted as I am often busy.<br>
Thank you to all the people in [https://github.com/iam-py-test/my_filters_001/blob/main/CONTRIBUTORS.md](https://github.com/iam-py-test/my_filters_001/blob/main/CONTRIBUTORS.md) for helping improve these filters.<br>
For uBlock Origin users, you can right click on any link starting with `https://subscribe.adblockplus.org`, click "uBlock Origin", then "Subscribe to filterlist...":<br>
<img src="https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/wiki/right%20click%20to%20add.jpg" alt="The Firefox context menu when clicking on a filterlist subscribe link, showing the uBlock Origin options"><br>
This image shows the Firefox context menu, but it should work in any browser supporting the latest version of uBo.

Please note! I am only one person, and I do not have much time to dedicate to this project. These lists _don't_ get updated as often as they should, and I'm sorry.

## Filters in this repo

#### Actively maintained
- The malicious website blocklist (antimalware.txt) ([Subscribe](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/antimalware.txt&title=The%20malicious%20website%20blocklist))

The Malicious Website Blocklist blocks malware, phishing, some scams, and Potentially Unwanted Programs (PUPs). Note the latter category includes legitimate websites which engage in deceptive practices.

#### Automatically generated
- DuckDuckGo Clean up (duckduckgo-clean-up.txt) - Generated from The malicious website blocklist and iam-py-test's anti-PUP list
- Brave Search Clean up (brave-clean-up.txt) - Generated from The malicious website blocklist and iam-py-test's anti-PUP list
- Everything in the _Alternative list formats_ folder
- [The Malicious Website Blocklist lite](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_lite.txt)


#### Actively maintained but don't require frequent updates
- [My anti-Facebook list](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/antifacebook.txt)
- Anti-Norton tracking list HOSTs file (anti-norton-tracking.txt)
- iam-py-test's Discord cleanup list ([discord_cleanup.txt](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/discord_cleanup.txt))
- DuckDuckGo Additional Cleanup ([duckduckgo_extra_clean.txt](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/duckduckgo_extra_clean.txt))
- Anti-Dynamic DNS ([antidynamicdns.txt](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/antidynamicdns.txt))
- IP Lookup service blocklist ([antiiplookup.txt](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/antiiplookup.txt))
- Anti-typosquatting list (antitypo.txt)
- Anti-redirectors list (anti-redirectors.txt)
- Anti-'page visit counter' list (anti-visit.txt)
- [iam-py-test's anti-PUP list](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/antipup.txt)

This is a more aggressive list which blocks:
- Snake oil programs such as registry cleaners
- Low quality malware removal guides
- Bundled software installers

#### Extension lists which add on to my existing lists
- [The malicious website blocklist - uBlock Origin extension](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/anti-malware-ubo-extension.txt)

#### Updated rarely but still technically supported
- My anti-rickroll list (anti-rickroll-list.txt)
- The clickbait blocklist (clickbait.txt) ([Subscribe](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/clickbait.txt&title=Clickbait%20Blocklist))
- [Google Safe Browsing reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/google-safe-browsing-reverse-engineered.txt)
- [Microsoft Smart Screen reverse-engineered](https://github.com/iam-py-test/my_filters_001/blob/main/special_lists/microsoft-smart-screen-reverse-engineered.txt)

#### Lists for testing syntax
- Everything in the _Sandbox_ folder
- The useless filter list (useless-list.txt)
- test_filter.txt

#### Lists which I gave up on
- Pornography Blocklist (porn.txt) <br>
This list [has been unmaintained since 2021](https://github.com/iam-py-test/my_filters_001/commits/main/porn.txt), and many of the domains listed are either dead or false positives. I have no plans of adding new entries or removing invalid/dead ones. Use at your own risk (or not at all, there are far better actively maintained lists).
- The device privacy list (device_privacy.txt)
- Anti-cookie-consent and paywalls list (anti-cookie+sign up.txt)
- [My Enhanced Protection list](https://github.com/iam-py-test/my_filters_001/blob/main/enhanced_protection.txt) (Warning: This list is pretty much unmaintained and very poorly thought out)
- Annoyances (annoyances.txt)
- Anti-'JavaScript is disabled' warnings (no-js-warnings.txt)
- "Personal filters" (iam-py-test.txt)
- "Lockdown mode"

#### Dead lists which are not even complete
- trojan_protection_list.txt
- Anti-over-promoted Windows antivirus list (could not find enough instances of this that would not break legitimate websites)
- anti-cookie+sign up_extention.txt (had one purpose - to work with my custom scriptlets - but the website it was intended to work for changed cookie values to quickly for it to work). Also, the filename is misspelled.
- Anti-adfly (anti-adfly.txt)
This list is no longer maintained, as adfly has been bought by Linkverse.
- Link redirect removal list (redirect-remover.txt)
- Favicon blocker ([favicon_blocker.txt](https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/favicon_blocker.txt))
- Anti-TikTok ([anti-tiktok.txt](./anti-tiktok.txt))
- Anti-dating ([antidating.txt](./antidating.txt))
- Anti-file hosting/shareing websites ([anti-file-hosting.txt](./anti-file-hosting.txt))
- Anti-"Private analytics" ([anti-privacy-analytics.txt](./anti-privacy-analytics.txt))
- TLD blocking lists ([more information](https://github.com/iam-py-test/my_filters_001/tree/main/region_blocklist))

<br>The filters in the _Alternative list formats_ folder are versions of some of the lists above for different software. These are auto-generated, and thus updates to them must be made to the original list or [the Python script](https://github.com/iam-py-test/my_filters_001/blob/main/scripts/update.py) which generates them.<br>
Everything not listed above, like the filters in the _Personal_ folder, is either completely forgotten by me, or is likely to break websites due to its purpose or lack of regulation. <br>

## Other formats

#### The malicious website blocklist
- HOSTs format - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_hosts.txt
- Domains only - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_domains.txt
- IP Addresses only - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_ips.txt
- AdGuard Windows/MacOS - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_adguard_app.txt
- AdGuard Home - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_adguard_home.txt
- dnsmasq (untested) - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_dnsmasq.txt
- JSON - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_json.json
- HOSTs format (no comments) - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_pure_hosts.txt
    - **Warning:** [Windows can not handle large HOSTs files. Some configuration changes may be needed if you experience issues](https://github.com/StevenBlack/hosts?tab=readme-ov-file#warning-using-this-hosts-file-in-windows-may-require-disabling-dns-cache-service)
- AdBlock Plus format (not recommended) - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_abp.txt
    - ABP lacks the ability to completely block access to websites, and thus this filter is largely ineffective.

#### Clickbait blocklist (unmaintained)
- AdBlock Plus format - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_abp.txt
- Domains only - https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/clickbait_domains.txt

#### Pornography Blocklist (unmaintained)
- HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_hosts.txt
- AdBlock Plus format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_abp.txt
- Domains only (i.e., PiHole) - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_domains.txt
- Pure (no comments) HOSTs format - https://github.com/iam-py-test/my_filters_001/blob/main/Alternative%20list%20formats/porn_pure_hosts.txt

## Projects which use my lists
- [pallebone's PersonalPiholeListsPAllebone](https://github.com/pallebone/PersonalPiholeListsPAllebone) uses the domains version of the malicious website blocklist
- [eded333's TheF\*ckingList](https://github.com/eded333/TheFuckingList) uses the uBlock Origin version of the Malicious Website Blocklist and the Anti-Norton Tracking list
- [hagezi's DNS Blocklists](https://github.com/hagezi/dns-blocklists) use the domains version of the Malicious Website Blocklist, "my" clickbait list, VXVault filter, and my Anti-Dynamic DNS list.
- [The oisd blocklist](https://oisd.nl) includes my antitypo list in their full list, and my Porn blocklist in their NSFW list
- [T145's Black Mirror](https://github.com/T145/black-mirror) includes the Malicious Website Blocklist
## Mentions
- [fynks's extension configuration](https://github.com/fynks/configs#extension-configs-)
- [yokoffing's recommended lists](https://github.com/yokoffing/filterlists#security)
- [From blocking ads to blocking anything – how to master the uBlock Origin configuration](https://www.osintme.com/index.php/2023/11/30/from-blocking-ads-to-blocking-anything-how-to-master-the-ublock-origin-configuration/)

These are not endorsements of these lists or guides. 

#### Notes
- The DuckDuckGo Clean Up list is auto-generated from duckduckgo-clean-up.template and the domains/ips versions of The malicious website blocklist. Changes in Pull Requests should be made to The malicious website blocklist or to [the Python script](https://github.com/iam-py-test/my_filters_001/blob/main/scripts/update-duckduckgo-clean-up.py). 
- Like above, The Brave Search Clean Up list is auto-generated from brave-clean-up.template and the domains/ips versions of The malicious website blocklist. Changes in Pull Requests should be made to The malicious website blocklist or [the Python script](https://github.com/iam-py-test/my_filters_001/blob/main/scripts/update-brave-clean-up.py).
- Google Safe Browsing reverse engineered and Microsoft Smartscreen reverse engineered _are not_ intended as lists of known malware domains, instead they are lists of domains/urls which are blocked by those services in an attempt to understand them and provide some of their protection to users of other browsers. They are also rarely updated
- All the up-to-date HOSTs versions use 0.0.0.0 instead of 127.0.0.1, as per [#87](https://github.com/iam-py-test/my_filters_001/issues/87)
- The _domains_lite_ and _hosts_lite_ versions are unmaintained as they took too much time to create and the script(s) which made them have been lost to history, however, the antimalware_lite is not.
- _The malicious website blocklist - uBlock Origin extension_ should not be installed on its own as it is designed only to be included in _The malicious website blocklist_.
