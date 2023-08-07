Write-Host "The System Hijack Removal Tool (2)"
Write-Host "This tool will try to remove known malware"
Read-Host "Press enter to continue" | Out-Null

$should_create_restore = (Read-Host "Create system restore point (y/n)?")
if($should_create_restore -eq "y"){
    try{
        Checkpoint-Computer -Description 'System Hijack Removal Tool - before run' -RestorePointType 'MODIFY_SETTINGS'
    }
    catch{
        Write-Host "Could not create system restore point"
        $should_enable = (Read-Host "Enable system restore (y/n)?")
        if($should_enable -eq "y"){
            Enable-ComputerRestore -Drive "$env:systemdrive\"
        }
    }
}

$security_software_filenames = @("mbam.exe", "msert.exe", "taskmgr.exe", "eav_trial_rus.exe", "eis_trial_rus.exe", "essf_trial_rus.exe", "hitmanpro_x64.exe", "ESETOnlineScanner_UKR.exe", "ESETOnlineScanner_RUS.exe", "HitmanPro.exe", "Cezurity_Scanner_Pro_Free.exe", "Cube.exe", "AVbr.exe", "AV_br.exe", "KVRT.exe", "cureit.exe", "FRST64.exe", "eset_internet_security_live_installer.exe", "esetonlinescanner.exe", "eset_nod32_antivirus_live_installer.exe", "PANDAFREEAV.exe", "bitdefender_avfree.exe", "drweb-12.0-ss-win.exe", "Cureit.exe", "TDSSKiller.exe", "KVRT(1).exe", "rkill.exe", "adwcleaner.exe", "frst.exe", "frstenglish.exe", "combofix.exe", "iexplore.exe", "msconfig.exe", "jrt.exe", "mbar.exe", "SecHealthUI.exe")
$procs_to_kill = @("sOFvE", "aspnet_compiler", "ZBrWfxmlCHpYeX", "n2770812", "legola", "pdates", "applaunch", "jsc", "wscript", "cscript", "csc", "usjhlmmdmsqjfbox", "bstyoops", "Setup_File", "timeout", "hydra", "Endermanch@Hydra", "processhider", "Endermanch@Hydra", "c5892073", "ratt", "rundll32", "lll", "livess", "atonand", "rft64", "MsiExec", "Launcher", "AddInUtil", "wordpad", "x9943392", "pdates", "bs1", "cacls", "rundll32", "calc", "winlogson", "schtasks", "autoit", "autoit3", "0a29ee64b40a3adb3f5a5e1815c5de53", "b78f9dc987653121104c5eaa55ab8d4a", "fe2c051a9160b6207a186110b585a5b8", "TotalUninstall", "	Total Uninstall Professional","totalav", "spyhunter", "regclean", "mssconfig", "mscnfig", "393", "aafg31", "more", "bot")
$locs_to_kill = @("$env:APPDATA", "$env:TEMP")
$systemdirs = @("$env:windir\System32".ToLower(),"$env:windir".ToLower(), "$env:windir\syswow64".ToLower())

# https://stackoverflow.com/a/63344749
if(!([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
 Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList "-File `"$($MyInvocation.MyCommand.Path)`"  `"$($MyInvocation.MyCommand.UnboundArguments)`""
 Exit
}

$procs = (Get-Process)
foreach($proc in $procs){
    $procpath = $proc.Path
    if($procpath -eq $null){
        continue
    }
    if($procs_to_kill.Contains($proc.Name)){
        Write-Host "Killed $procpath"
        $proc.kill()
    }
    $rootdir = (Split-Path ($procpath)).ToLower()
    if($locs_to_kill.Contains($rootdir)){
        $proc.kill()
        Write-Host "Killed $procpath"
    }
    if($proc.Name -eq "winlogon"){
        if($systemdirs.Contains($rootdir)){

        }
        else{
            $proc.kill()
        }
    }
    if($procpath.Contains(".pif")){
        $proc.kill()
    }
}

$iefo = (Get-ChildItem "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options")
foreach($subiefo in $iefo){
    $dbgval = (Get-ItemProperty ($subiefo).PSPath).Debugger
    $subiefoname = $subiefo.Name
    $subiefocname = $subiefo.PSChildName
    if($security_software_filenames.Contains($subiefocname)){
        if((Get-ItemProperty ($subiefo).PSPath).PSobject.Properties.name -match "Debugger"){
             Remove-ItemProperty -Path ($subiefo).PSPath -Name "Debugger"
             Write-Host "Unblocked $subiefocname"
        }
    }
    
}

$disallowrun_path = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
$disallowrun = (Get-ItemProperty $disallowrun_path)
foreach($subprop in $disallowrun){
    $dar = ""
    $darname = ""
    foreach($p in $subprop.PSObject.Properties){
        echo $p
        if($p.Name.StartsWith("PS")){
            echo "ignored"
        }
        else{
            $dar = $p.Value
            $darname = $p.Name
        }
    }
    echo $dar $darname
    if($security_software_filenames.Contains($dar)){
        Remove-ItemProperty -Path $disallowrun_path -Name $darname
        Write-Host "Unblocked $dar"
    }
}

Write-Host "Repairing Windows Defender"
$defender_exc_paths = (Get-Mppreference).ExclusionPath
foreach($expath in $defender_exc_paths){
    Remove-MpPreference -ExclusionPath $expath
}
$defender_exc_ext = (Get-Mppreference).ExclusionExtension
foreach($ext in $defender_exc_ext){
    Write-Host "Removed exclusion for $ext"
    Remove-MpPreference -ExclusionExtension $ext
}
Set-MpPreference -DisableArchiveScanning $false -Force
Set-MpPreference -PUAProtection 1
Set-MpPreference -UILockdown $false
Set-MpPreference -DisableAutoExclusions $true
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"

Set-Service WinDefend -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service Bits -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service trustedinstaller -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service bits
Start-Service WinDefend -ErrorAction SilentlyContinue

Update-MpSignature
Start-MpScan -ScanType QuickScan

Write-Host "Turning on Windows Firewall"
Set-Service BFE -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service mpsdrv -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service mpssvc -StartupType Automatic -ErrorAction SilentlyContinue
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

Write-Host "Checking for damaged system files"
sfc /scannow

Write-Host "Removing unwanted browser changes"
Remove-ItemProperty -Path "HKCU:\Software\Policies\Google\chrome" -Name "DownloadRestrictions"
Remove-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Edge" -Name "DownloadRestrictions"

Write-Host "Removing known malware"
Remove-Item "$env:systemdrive\Windows\Fonts\*" -Include "*.exe"
Remove-Item "$env:public\AccountPictures\*" -Include "*.exe"
Remove-Item "HKCU:\Software\Conduit" -Recurse -Force -ErrorAction SilentlyContinue
$filesinroaming = (Get-ChildItem $env:appdata)
foreach($file in $filesinroaming){
    $root = Split-Path "$env:appdata\$file"
    if($root -eq $env:appdata){
        if($file.Name.EndsWith(".exe")){
            Write-Host "$root $env:appdata\$file"
        }
    }
}
$knownmalware = @("$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\eNXtBTKShU.url", "$env:systemdrive\Users\Public\Viyeinmz.url", "$env:systemdrive\Users\Public\Owhgjnta.url", "$env:systemdrive\ProgramData\Default\cDefaultc.vbs", "$env:systemdrive\Windows\system32\config\systemprofile\AppData\Roaming\winlogon.exe", "$env:systemdrive\Program Files\WindowsPowershell\RuntimeBroker.exe", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\ratt.exe", "C:\Windows\rft64.exe", "C:\WINDOWS\SYSTEM32\TASKS\GoogleUpdateTaskMachineQC", "C:\PROGRAM FILES\GOOGLE\CHROME\UPDATER.EXE", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\Scanned.js")
foreach($malware in $knownmalware){
    if(Test-Path "$malware"){
        Remove-Item "$malware"
        Write-Host "Removed $malware"
    }
}
$knownmalwaredirs = @("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Auslogics", "C:\WINDOWS\SYSTEM32\TASKS\jjrcjc", "c:\ProgramData\Microsoft\IObitUnlocker", "c:\ProgramData\WindowsTask", "C:\Programdata\Microsoft\wjqqg", "C:\ProgramData\Dllhost")
foreach($malware in $knownmalwaredirs){
    if(Test-Path "$malware"){
        Remove-Item -Recurse -Force "$malware"
        Write-Host "Removed $malware"
    }
}

Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" -Name "Startup" -Value "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "Shell" -Value "explorer.exe"
New-Item -Path "Registry::HKEY_CLASSES_ROOT\.exe" -ErrorAction silentlyContinue
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\.exe" -Name "(default)" -Value "exefile"
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile" -ErrorAction silentlyContinue
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell" -ErrorAction silentlyContinue
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell\runas" -ErrorAction silentlyContinue
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell\runas\command" -ErrorAction silentlyContinue
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell\runas\command" -Name "(default)" -Value "`"%1`" %*"
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell\open" -ErrorAction silentlyContinue
New-Item -Path "Registry::HKEY_CLASSES_ROOT\exefile\shell\open\command" -ErrorAction silentlyContinue
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\exefile\open\runas\command" -Name "(default)" -Value "`"%1`" %*"
Remove-Item -Path HKCU:\SOFTWARE\Classes\mscfile\shell\open\command
Remove-Item -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate
Remove-Item -Path HKCU:\SOFTWARE\Classes\.exe
Remove-Item -Path HKCU:\SOFTWARE\Classes\.reg
bcdedit.exe /set "{default}" recoveryenabled yes
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SafeBoot" -Name "AlternateShell" -Value "cmd.exe"
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "DisableTaskMgr"
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "DisableRegistryTools"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "PromptOnSecureDesktop" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorUser" -Value 3
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 3

Write-Host "Resetting network settings"
NETSH winsock reset catalog
NETSH int ipv4 reset reset.log
NETSH int ipv6 reset reset.log
netsh int ip reset
netsh winsock reset
netsh winhttp reset proxy
ipconfig /flushdns

Write-Host "Clearing temp files..."
bitsadmin /reset /allusers | Out-Null
$tempfolders = @("$env:userprofile\APPDATA\LOCAL\MICROSOFT\WINDOWS\INETCACHE\IE\", "$env:temp", "$env:appdata\Microsoft\Windows\Recent", "$env:systemdrive\Windows\Temp")
foreach($temploc in $tempfolders){
    Get-ChildItem $temploc -Exclude "system_hijack_removal_tool.ps1" | Remove-Item -Recurse -Force
    Write-Host "Cleared $temploc"
}
Remove-Item "$env:systemdrive\Windows\Prefetch\*" -Include "*.pf"
Clear-RecycleBin -Force

Write-Host "You need to reboot your system"
Read-Host "Press enter to end" | Out-Null
