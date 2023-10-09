## Contributing
Please contribute. _Please_. Maintaining a filterlist is not an easy thing and I can only spend a finite amount of time on maintaining a filterlist. I welcome contributions, even if they are just to fix a typo or remove a redundant entry.

#### Rules
Please be respectful to other people even if their beliefs or opinions differ from yours. <br/>
Before opening an issue, please be sure there is not another issue open about the exact same thing. If there is, you can add your opinion or fix to that issue's comments. <br/>
If your issue was closed as `invalid`, please avoid immediately opening another issue without correcting the problem. Doing so will result in that issue being closed as well. Before opening an issue, please check https://github.com/iam-py-test/my_filters_001/blob/main/wiki/incompatible.md to ensure the issue is not a conflict. <br/>
Please understand that I am only one person, and that I will not be able to respond to or correct your issue immediately. If something is important, please @ reference me in that issue and I will check it out.<br/>
Please follow the [GitHub Community Guidelines](https://docs.github.com/en/github/site-policy/github-community-guidelines#what-is-not-allowed) or else you will be banned from this Repo and reported to GitHub. Internet pranks - including rickrolling - are prohibited and may result in a ban after repeated violations. <br/>

I will currently not be accepting issues for server-side paywalls (unless you have a fix) as there is **nothing** I can do about them. <br>

Please open a pull request or issue instead of commenting on commits, as I am unlikely to see commit comments, but regularly check for issues.

### MV3 note
I can - and never will - support Google's Manifest V3 as it will destroy all content blocking. If you don't like that, talk to Google. Any issues caused by Manifest V3 will be closed as _can't fix_. I strongly recommend you switch to a non-Chromium browser like Tor Browser or Firefox. 

### Note about Internet Explorer
I do not - and never will - support Microsoft's Internet Explorer, as it is a complete mess, and isn't even maintained. I recommend you switch to any maintained browser, as Microsoft won't fix any issues with IE, and it is therefore broken and insecure.

### Opera
Opera prevents extensions from accessing search result pages. To allow access, open opera://extensions/ and check the "allow access to search page results" option. Thanks to the uBo team for informing me (and other people) of this. 

### kiwi browser
Kiwi browser [is not supported by uBlock Origin](https://github.com/uBlockOrigin/uBlock-issues/issues/2791), and thus my filterlists (I am not sure about other content blockers). Be aware that Kiwi browser [disables extensions](https://www.reddit.com/r/uBlockOrigin/comments/10xntsr/comment/j7teo9p/) on [a long list of domains](https://github.com/kiwibrowser/src/blob/c51d640a8e984ff0fb24049c53a7ed4e458775ef/extensions/browser/api/web_request/web_request_permissions.cc#L167). Note that this also includes **any** domain containing `bing.com`, `search.yahoo.`, and some other tokens, meaning extensions may be disabled on other websites (such as malware and scam sites).
For this reason, [alleged privacy issues](https://github.com/Tobi823/ffupdater/issues/35), and [the lack of frequent updates](https://github.com/kiwibrowser/src.next/commits/kiwi) ([including slow response times to vulnerabilities](https://github.com/kiwibrowser/src.next/issues/1001)), I would recommend against using this browser.

### Yandex
Yandex Browser is not supported by uBlock Origin (I do not know about other content blockers), [and is known to be problematic](https://github.com/uBlockOrigin/uBlock-issues/issues/2627). Any issues which can not be reproduced in Chrome, Edge, or Firefox will have to be investigated by you.
