## Fix browser-based malware
Browser-based malware is fairly common now days. This guide should help remove a few of the most common types.

### Remove spam notifications
Malicious websites can send you spammy notifications, such as fake warnings about malware: <br>
<img src="spam notifiation 1.jpg" width=300 height=300>
<img src="notification spam 2.jpg" width=300 height=300>

Revoke the ability to send notifiations for all but sites which need it and which you trust:
- Chrome: https://support.google.com/chrome/answer/114662 (under Learn about permissions that can be changed, then scroll down)
- Firefox: https://support.mozilla.org/en-US/kb/push-notifications-firefox#w_how-do-i-revoke-web-push-permissions-for-a-specific-site ([Firefox for Android](https://support.mozilla.org/en-US/kb/manage-notifications-firefox-android))
- Edge: https://products.support.services.microsoft.com/en-us/microsoft-edge/manage-website-notifications-in-microsoft-edge-0c555609-5bf2-479d-a59d-fb30a0b80b2b

If that does not work or you want to be sure, clear your browser cache and site data, which should remove the code which is causing these issues: <br>
**Warning: This will sign you out of websites and may clean temporary data (settings, shopping carts) on some websites**<br>
- Firefox: https://support.mozilla.org/en-US/kb/clear-cookies-and-site-data-firefox
- Chrome: https://support.google.com/accounts/answer/32050
- Edge: https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09 (chose "delete all cookies")

### Change search engine and homepage/new tab
Some malware will only change your homepage/new tab or search engine, and will not prevent you from changing it back <br>
Homepage/new tab:
- Firefox: https://support.mozilla.org/en-US/kb/how-to-set-the-home-page
- Chrome: https://support.google.com/chrome/answer/95314
- Edge: https://support.microsoft.com/en-us/microsoft-edge/change-your-browser-home-page-a531e1b8-ed54-d057-0262-cc5983a065c6 (also has steps for other browsers, but they may not be up-to-date)
<br>Search engine:
- Firefox: https://support.mozilla.org/en-US/kb/change-your-default-search-settings-firefox
- Chrome: https://support.google.com/chrome/answer/95426
- Edge: https://support.microsoft.com/en-us/microsoft-edge/change-your-default-search-engine-in-microsoft-edge-cccaf51c-a4df-a43e-8036-d4d2c527a791
<br>If your browser says the homepage or search engine is managed by an extension, follow [the instructions below to uninstall that extension](#uninstall-a-specific-extension).

### Uninstall a specific extension
If a specific extension is causing problems, you can uninstall it: 
- Firefox: https://support.mozilla.org/en-US/kb/disable-or-remove-add-ons
- Chrome: https://support.google.com/chrome_webstore/answer/2664769
- Edge: https://support.microsoft.com/en-us/microsoft-edge/add-turn-off-or-remove-extensions-in-microsoft-edge-9c0ec68c-2fbc-2f2c-9ff0-bdc76f46b026
In some cases, extensions can not be removed or reappear. If that happens, see [Dealing with agressive malware](#dealing-with-agressive-malware). If you are unsure what extensions to uninstall, see if you have [any of the extensions listed below](#known-malware-browser-extensions) installed, and if so, try uninstalling them.

#### Known malware browser extensions
If installed, I recommend you remove these. However, this is not an exhaustive  list.
- "Browsing Overview by Securify"
Changes your search engine to `search[.]mysecurify[.]com`, which redirects to Bing.

### Remove malware from your system
Windows:
- Adwcleaner: https://support.malwarebytes.com/hc/en-us/articles/360038520114-Malwarebytes-AdwCleaner-scan-and-clean (do not remove any of the "preinstalled software" unless you know what you are doing; it is **not** malware)

### Dealing with agressive malware
Before continuing, try the steps for removing malware on your system. 
