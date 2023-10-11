echo Minor Windows hardening
pause

rem Remove malware
del /F %appdata%\*.exe

rem https://support.huntress.io/hc/en-us/articles/12353342482195
rem https://www.youtube.com/watch?v=tu6FzFfzhF4
mkdir %systemdrive%\INTERNAL
echo "Protected" > %systemdrive%\INTERNAL\__EMPTY

rem https://malicious.link/post/2022/blocking-iso-mounting/
reg add HKCR\Windows.IsoFile\shell\mount /v ProgrammaticAccessOnly /d 1 /t REG_SZ

rem soon to be default: https://www.bleepingcomputer.com/news/security/microsoft-to-kill-off-vbscript-in-windows-to-block-malware-delivery/
taskkill /F /IM "wscript.exe"
taskkill /F /IM "cscript.exe"
reg add "HKLM\SOFTWARE\Microsoft\Windows Script Host\Settings" /v Enabled /d 0 /t REG_DWORD /f
reg add "HKCU\SOFTWARE\Microsoft\Windows Script Host\Settings" /v Enabled /d 0 /t REG_DWORD /f

pause