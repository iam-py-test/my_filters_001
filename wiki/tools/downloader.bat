@echo off
echo Killing processes...
taskkill /F /IM "powershell.exe"
taskkill /F /IM "curl.exe"

echo Unblock raw.githubusercontent.com
attrib -S C:\Windows\System32\drivers\etc\hosts
attrib -R -H C:\Windows\System32\drivers\etc\hosts
copy C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.downloader.backup
type C:\Windows\System32\drivers\etc\hosts | find /V "raw.githubusercontent.com" > C:\Windows\System32\drivers\etc\hosts
ipconfig /flushdns

echo Downloading...
del /F "%temp%\system_hijack_removal_tool.ps1" 
curl "https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/wiki/tools/system_hijack_removal_tool.ps1" --output "%temp%\system_hijack_removal_tool.ps1"
powershell -executionpolicy bypass "%temp%\system_hijack_removal_tool.ps1"
del /F "%temp%\system_hijack_removal_tool.ps1"
echo Done
pause
