@echo off
curl "https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/wiki/system_hijack_removal_tool.ps1" --output "%temp%\system_hijack_removal_tool.ps1"
powershell -executionpolicy bypass "%temp%\system_hijack_removal_tool.ps1"
del /F "%temp%\system_hijack_removal_tool.ps1"
