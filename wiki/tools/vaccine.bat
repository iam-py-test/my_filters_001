echo Lockdown Windows
pause

rem https://support.huntress.io/hc/en-us/articles/12353342482195
rem https://www.youtube.com/watch?v=tu6FzFfzhF4
mkdir %systemdrive%\INTERNAL
echo "Protected" > %systemdrive%\INTERNAL\__EMPTY

rem https://malicious.link/post/2022/blocking-iso-mounting/
reg add HKCR\Windows.IsoFile\shell\mount /v ProgrammaticAccessOnly /d 1 /t REG_SZ

pause