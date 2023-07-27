@echo off

rem https://stackoverflow.com/a/69794302
@echo off
if "%1"=="runas" (
  cd %~dp0
  echo Killing all browsers...
) else (
  powershell Start -File "cmd '/C %~f0 runas'" -Verb RunAs
  exit
)

rem Firefox
taskkill /F /IM "firefox.exe"

rem Chrome
taskkill /F /IM "chrome.exe"
taskkill /F /IM "GoogleCrashHandler.exe"
taskkill /F /IM "GoogleCrashHandler64.exe"

rem Edge
taskkill /F /IM "msedge.exe"

rem Brave
taskkill /F /IM "brave.exe"
taskkill /F /IM "BraveCrashHandler.exe"
taskkill /F /IM "BraveCrashHandler64.exe"

rem Opera
taskkill /F /IM "opera.exe"
taskkill /F /IM "opera_crashreporter.exe"
taskkill /F /IM "opera_autoupdate.exe"

rem OperaGX
taskkill /F /IM "OperaGXSetup.exe"

rem Yandex
taskkill /F /IM "yandex.exe"

echo All browsers killed
