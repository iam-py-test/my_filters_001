## Fix browser-based malware
Browser-based malware is fairly common now days. This guide should help remove a few of the most common types.

Warning: This is a work in progress!

### Things not to do
- Do not use "cleaner" programs to clear browser cache/cookies. These programs may cause problems with your browser. Use your browser settings to clear cookies and cache.

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
In some cases, extensions can not be removed or reappear. If that happens, [make sure browser sync is not restoring them](#reset-browser-sync).
If you are unsure what extensions to uninstall, see if you have [any of the extensions listed below](#known-malware-browser-extensions) installed, and if so, try uninstalling them. You also can try disabling your extensions one-by-one and seeing which one is causing the problem.

#### Known malware browser extensions
If installed, I recommend you remove these. However, this is not an exhaustive  list.
- "Browsing Overview by Securify"
Changes your search engine to `search[.]mysecurify[.]com`, which redirects to Bing.

### Remove a theme
Themes should not be able to do anything bad (to my knowledge), are rarely ever are malware. However, should you want to remove them, here is how:
- Chrome: https://support.google.com/chrome_webstore/answer/148695
- Edge: https://www.howtogeek.com/725974/how-to-add-and-remove-themes-in-microsoft-edge/ (unoffical guide, instructions are under "How to Remove or Uninstall Themes from Microsoft Edge")

### Reset browser sync
Many browsers now have the ability to sync data between devices. This feature sadly has the side effect of causing unwanted browser changes to reappear, even after being removed. **Be aware that clearing your sync data probably will cause some synced data to be lost. Be sure to save any important data (i.e. passwords) securely outside your browser just in case.**<br>
- Chrome: https://forums.malwarebytes.com/topic/258886-chrome-secure-preferences-detection-always-returns/ (this is a good guide made by people who know what they are doing)
- Edge (didn't find a good online guide): <br>
<details>
<summary>How to clear sync data in Edge</summary>
<ul>
<li>Open edge://settings</li>
<li>Click "Profiles" in the sidebar</li>
<li>Click "Sync"</li>
<li>Scroll down and click on "Reset sync"</li>
<li>You will be prompted to confirm. Click "reset"</li>
<li>Edge will reset your sync. It may take a short time for it to setup again (no action from you is needed)</li>
</ul>
</details>
I do not use sync on Firefox, so not sure this will help at all. Deleting your account will clear all data, but probably isn't ideal.
- Firefox sync: https://support.mozilla.org/en-US/kb/delete-sync-data-firefox-signing-out-firefox-account

### Remove malware from your system
Windows:
- Adwcleaner: https://support.malwarebytes.com/hc/en-us/articles/360038520114-Malwarebytes-AdwCleaner-scan-and-clean (do not remove any of the "preinstalled software" unless you know what you are doing; it is **not** malware)

### Remove browser policies (Windows)
Open regedit and delete these keys:
- Edge (current user):
    - HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Edge
    - HKEY_CURRENT_USER\SOFTWARE\WOW6432Node\Policies\Microsoft\Edge
- Edge (system) - you will need to run regedit as admin:
    - HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge
    - HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Policies\Microsoft\Edge
- Chrome (current user):
    - HKEY_CURRENT_USER\SOFTWARE\Policies\Google\Chrome
- Chrome (system) - you will need to run regedit as admin:
    - HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome 

### Reset your browser
- Chrome: https://support.google.com/chrome/answer/3296214
- Firefox: https://support.mozilla.org/en-US/kb/reset-preferences-fix-problems
- Edge (I do not see a good online guide for Edge)<br>
<details>
<summary>How to reset Edge</summary>
<ul>
<li>Go to edge://settings</li>
<li>Click "Reset settings" in the sidebar</li>
<li>Click "Restore settings to their default values"</li>
<li>You will be prompted to confirm. Click "reset"</li>
<li>Edge will be reset. All extensions will be disabled, but not uninstalled</li>
</ul>
</details>

### Dealing with agressive malware
Before continuing, try all the prior steps. This is the "nuclear" option. It will remove most/all data, so be sure you have anything (passwords, bookmarks) backed up. I do not have good guides for all browsers.
- MacOS (Safari and Chrome): https://forums.malwarebytes.com/topic/236261-how-to-remove-the-after-effects-of-adware/
- Windows/Chrome: https://forums.malwarebytes.com/topic/258938-resetting-google-chrome-to-clear-unexpected-issues/
- Windows/Edge: https://www.tenforums.com/tutorials/159010-how-completely-reset-microsoft-edge-chromium-default-windows.html (**Warning**: ALL data in ALL Edge profiles will be deleted!)
<br>If there is more than one user on the system, you may need to repeat some of these steps for each user.
