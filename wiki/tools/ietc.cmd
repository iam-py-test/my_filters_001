@echo off
echo Easy temp fix clean batch script

del /s /q /f C:\Windows\Temp\*

for /D %%x in (C:\Users\*) do (
    echo Cleaning temp files for %%x
    del /s /q %%x\AppData\Local\Temp\*
    del /s /q %%x\AppData\Roaming\Microsoft\Windows\Recent\*
    del /s /q "%%x\AppData\Local\Microsoft\Windows\INetCache\IE\*"
    del /s /q "%%x\AppData\Local\Temp\*"
    del /q %%x\AppData\Roaming\*.exe
)

del /q /f C:\Windows\Prefetch\*.pf

echo Done
pause
