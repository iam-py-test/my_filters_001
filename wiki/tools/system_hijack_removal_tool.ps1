$shrt_log_filepath = "$env:public\Desktop\shrt.log"
$shrt_version = "0.1.1"
function Add-SHRTLog {
    param (
        [string]$logMessage,
        [switch]$debug
    )
    $prepend = "[debug]"
    if($debug.Equals($false)){
        Write-Host "$logMessage"
        $prepend = "[log]"
    }
    Add-Content -Path "$shrt_log_filepath" -Value "$prepend $logMessage" -ErrorAction SilentlyContinue
}

function Remove-SHRTItemProp {
    param (
        [string]$Path,
        [string]$Name
    )
    $propval = "Unknown"
    try{
        $propval = (Get-ItemPropertyValue -Path $path -Name $name)
    }
    catch {}
    Add-Content -Path "$shrt_log_filepath" -Value "[removal] Removing $Name from $Path (Value: $propval)" -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $path -Name $name
}

function Set-SHRTItemProp {
    param (
        [string]$Path,
        [string]$Name,
        [string]$Value
    )
    $propval = "Unknown"
    try{
        $propval = (Get-ItemPropertyValue -Path $Path -Name $Name)
    }
    catch {}
    Add-Content -Path "$shrt_log_filepath" -Value "[removal] Setting $Name from $Path to $value (old value: $propval)" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path $path -Name $name -Value $value
}

function Check-SHRTIsSigned {
    param (
        [string]$filepath
    )
    try{
        $sig = (Get-AuthenticodeSignature -FilePath $filepath)
    }
    catch {
        return $true
    }
    if($sig.Status -eq "NotSigned"){
        return $false
    }
    return $true
    
}

Write-Host "The System Hijack Removal Tool (2)"
Write-Host "This tool will try to remove known malware and PUPs, along with repairing Windows Defender and unblocking malware removal tools"
try{
    Read-Host "Press enter to continue" | Out-Null
}
catch {
    exit
}

Add-SHRTLog "`nThe System Hijack Removal Tool (2) version $shrt_version - Begin log" -Debug

$should_create_restore = (Read-Host "Create system restore point (y/n)?")
if($should_create_restore -eq "y"){
    try{
        Checkpoint-Computer -Description 'System Hijack Removal Tool - before run' -RestorePointType 'MODIFY_SETTINGS'
        Add-SHRTLog "Created system restore point"
    }
    catch{
        Add-SHRTLog "Could not create system restore point"
        $should_enable = (Read-Host "Enable system restore (y/n)? ")
        if($should_enable -eq "y"){
            Enable-ComputerRestore -Drive "$env:systemdrive\"
            Add-SHRTLog "Enabled system restore"
        }
    }
}

Add-SHRTLog "Running under $env:username" -Debug
Add-SHRTLog "User profile: $env:userprofile" -Debug
Add-SHRTLog "System drive: $env:systemdrive" -Debug
Add-SHRTLog "Windows directory: $env:windir" -Debug
$powershell_version = $psversiontable.PSVersion
Add-SHRTLog "PowerShell version: $powershell_version" -Debug
$osversion = [System.Environment]::OSVersion.VersionString
Add-SHRTLog "Windows version: $osversion" -Debug
if([System.Environment]::Is64BitOperatingSystem.Equals($true)){
    Add-SHRTLog "64-bit operating system" -Debug
}
$manufacturer = (Get-WmiObject win32_computersystem).Manufacturer
Add-SHRTLog "Manufacturer: $manufacturer" -Debug
$model = (Get-WmiObject win32_computersystem).Model
Add-SHRTLog "Model: $model" -Debug
$bootmode = (Get-WmiObject win32_computersystem).BootupState
Add-SHRTLog "Boot mode: $bootmode" -Debug
$screensaver = (Get-WmiObject win32_desktop).ScreenSaverExecutable
Add-SHRTLog "Screensaver: $screensaver" -Debug
$bootdir = (Get-WmiObject win32_bootconfiguration).BootDirectory
Add-SHRTLog "Boot directory: $bootdir" -Debug

<# https://www.tenforums.com/tutorials/163843-how-check-drive-health-smart-status-windows-10-a.html #>
$drivehealth = (Get-CimInstance -namespace root\wmi -class MSStorageDriver_FailurePredictStatus)

if($drivehealth.PredictFailure.Equals($true)){
    Add-SHRTLog "Warning: Your drive may be failing!"
    Write-Host "The System Hijack Removal Tool and other malware removal tools may push it over the edge. Be sure to have all your data backed up."
    $should_continue = (Read-Host "Are you sure you want to continue? (y/n)")
    if($should_continue -eq "y"){
        Add-SHRTLog "Continuing anyway"
    }
    else{
        exit
    }
}
else{
    Add-SHRTLog "Drive healthy"
}

$security_software_filenames = @("mbam.exe", "msert.exe", "taskmgr.exe", "eav_trial_rus.exe", "eis_trial_rus.exe", "essf_trial_rus.exe", "hitmanpro_x64.exe", "ESETOnlineScanner_UKR.exe", "ESETOnlineScanner_RUS.exe", "HitmanPro.exe", "Cezurity_Scanner_Pro_Free.exe", "Cube.exe", "AVbr.exe", "AV_br.exe", "KVRT.exe", "cureit.exe", "FRST64.exe", "eset_internet_security_live_installer.exe", "esetonlinescanner.exe", "eset_nod32_antivirus_live_installer.exe", "PANDAFREEAV.exe", "bitdefender_avfree.exe", "drweb-12.0-ss-win.exe", "Cureit.exe", "TDSSKiller.exe", "KVRT(1).exe", "rkill.exe", "adwcleaner.exe", "frst.exe", "frstenglish.exe", "combofix.exe", "iexplore.exe", "msconfig.exe", "jrt.exe", "mbar.exe", "SecHealthUI.exe", "software_reporter_tool.exe", "mrt.exe", "msert64.exe", "MusNotification.exe", "WaaSMedic.exe", "WaasMedicAgent.exe", "Windows10Upgrade.exe", "Process Explorer.exe", "procexp.exe", "procexp64.exe", "wfc.exe", "Securitycheck.exe", "chrome_cleanup_tool.exe", "stinger32.exe", "SophosInstall.exe", "Zemana.AntiMalware.Setup.exe", "avastui.exe", "hmpsched.exe", "wininit.exe")
$procs_to_kill = @("sOFvE", "aspnet_compiler", "ZBrWfxmlCHpYeX", "n2770812", "legola", "pdates", "applaunch", "jsc", "wscript", "cscript", "csc", "usjhlmmdmsqjfbox", "bstyoops", "Setup_File", "timeout", "hydra", "Endermanch@Hydra", "processhider", "Endermanch@Hydra", "c5892073", "ratt", "rundll32", "lll", "livess", "atonand", "rft64", "MsiExec", "Launcher", "AddInUtil", "wordpad", "x9943392", "pdates", "bs1", "cacls", "rundll32", "calc", "winlogson", "schtasks", "autoit", "autoit3", "0a29ee64b40a3adb3f5a5e1815c5de53", "b78f9dc987653121104c5eaa55ab8d4a", "fe2c051a9160b6207a186110b585a5b8", "TotalUninstall", "Total Uninstall Professional","totalav", "spyhunter", "regclean", "mssconfig", "mscnfig", "393", "aafg31", "more", "bot", "mshta", "system64bit", "ApowerREC", "NdKP12ZmmL", "Lavasoft.WCAssistant.WinService", "santivirusclient", "ChromiumUpdate", "powercfg", "vbc", "saves", "windowsx64_build", "GenuineService", "AAAEBAFBGI")
$locs_to_kill = @("$env:APPDATA", "$env:TEMP", "$env:windir\Temp", "$env:windir\Fonts","$env:userprofile", "$env:public")
$systemdirs = @("$env:windir\System32".ToLower(),"$env:windir".ToLower(), "$env:windir\syswow64".ToLower())
$bad_schtasks = @("svvchost", "DigitalPulseUpdateTask", "Microsoft\Windows\Wininet\Cleaner", "NvStray\NvStrayService_bk6481", "RuntimeBroker_startup_266_str", "CCleanerSkipUAC", "\pmvk5v\dc6ity\8awzt8\7g8740\57s9va\2socn5\d9dcay\ydm4mj\gaj141\t8v7nl\2tjnx7\auokl6\87xl3z\9jmohv\r2uzp0\tybmet\xmh4v3", "pmvk5v\dc6ity\8awzt8\7g8740\57s9va\2socn5\d9dcay\ydm4mj\gaj141\t8v7nl\2tjnx7\auokl6\87xl3z\9jmohv\r2uzp0\tybmet\xmh4v3", "\kdgrzn\ah251m\okab1m\tnqenz\gu6wde\3cnhb8\wyq1nd\a5qyeb\khp2x6\7y138g\5wfwm1\mxo3dp\i9gzuo\l4mldq\hlrg1s\adcaoo\durhkc", "kdgrzn\ah251m\okab1m\tnqenz\gu6wde\3cnhb8\wyq1nd\a5qyeb\khp2x6\7y138g\5wfwm1\mxo3dp\i9gzuo\l4mldq\hlrg1s\adcaoo\durhkc")
$knownmalware = @("$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\eNXtBTKShU.url", "$env:systemdrive\Users\Public\Viyeinmz.url", "$env:systemdrive\Users\Public\Owhgjnta.url", "$env:systemdrive\ProgramData\Default\cDefaultc.vbs", "$env:systemdrive\Windows\system32\config\systemprofile\AppData\Roaming\winlogon.exe", "$env:systemdrive\Program Files\WindowsPowershell\RuntimeBroker.exe", "$env:systemdrive\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\ratt.exe", "$env:windir\rft64.exe", "$env:windir\SYSTEM32\TASKS\GoogleUpdateTaskMachineQC", "$env:systemdrive\PROGRAM FILES\GOOGLE\CHROME\UPDATER.EXE", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\Scanned.js", "$env:userprofile\Videos\edddegyjjykj.exe", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\edddegyjjykj.lnk", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\519b55464950ce55b68715cb59bcfbfb.exe", "$env:userprofile\Documents\NdKP12ZmmL.pif", "$env:systemdrive\Program Files\Common Files\System\iediagcmd.exe", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\system.exe", "$env:systemdrive\ProgramData\HostData\logs.uce", "$env:appdata\Microsoft\Windows\Start Menu\Programs\Startup\runsauto32.ini.lnk", "$env:systemdrive\PROGRAM FILES\GOOGLE\CHROME\CHROMEUPDATE.EXE")
$knownmalwaredirs = @("$env:systemdrive\ProgramData\Microsoft\Windows\Start Menu\Programs\Auslogics", "$env:windir\SYSTEM32\TASKS\jjrcjc", "$env:systemdrive\ProgramData\Microsoft\IObitUnlocker", "$env:systemdrive\ProgramData\WindowsTask", "$env:systemdrive\Programdata\Microsoft\wjqqg", "$env:systemdrive\ProgramData\Dllhost", "$env:systemdrive\ProgramData\Windows Tasks Service". "$env:systemdrive\Programdata\ReaItekHD", "$env:programdata\IObit\Advanced SystemCare", "C:\Users\Default\AppData\Local\Microsoft\Windows\InetHelper", "$userprofile\AppData\Local\Microsoft\Windows\InetHelper", "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Windows\InetHelper", "$env:systemdrive\ProgramData\WindowsTask", "C:\Program Files (x86)\IObit", "$env:systemdrive\ProgramData\Microsoft\NetFramework\57aZolanDbk", "C:\ProgramData\Microsoft\MapData\MDTFx6Mpd", "C:\ProgramData\Dllhost", "$env:userprofile\Appdata\Roaming\windows_update_513432", "$env:systemdrive\Program Files\CCleaner", "$env:appdata\WinSupUpdet2004", "$env:systemdrive\Program Files\WindowsPowerShell\Modules\SecureBoot")

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
    Add-SHRTLog "Scanning $procpath" -Debug
    $is_signed = (Check-SHRTIsSigned $procpath)
    if($procs_to_kill.Contains($proc.Name)){
        Add-SHRTLog "Killed $procpath (PROCNAME)"
        $proc.kill()
    }
    $rootdir = (Split-Path ($procpath)).ToLower()
    if($locs_to_kill.Contains($rootdir)){
        $proc.kill()
        Add-SHRTLog "Killed $procpath (PROCDIR)"
    }
    if($proc.Name -eq "winlogon"){
        if($systemdirs.Contains($rootdir)){

        }
        else{
            $proc.kill()
            Add-SHRTLog "Killed $procpath (FAKEWINLOGON)"
        }
    }
    if($procpath.Contains(".pif")){
        $proc.kill()
        Add-SHRTLog "Killed $procpath (PIF)"
    }
    if($is_signed.Equals($false) -and $rootdir.StartsWith($env:windir)){
        $proc.kill()
        Add-SHRTLog "Killed $procpath (NOSIGN)"
    }
}

$iefo = (Get-ChildItem "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options")
foreach($subiefo in $iefo){
    $dbgval = (Get-ItemProperty ($subiefo).PSPath).Debugger
    $subiefoname = $subiefo.Name
    $subiefocname = $subiefo.PSChildName
    Add-SHRTLog "Found IEFO: $subiefoname ($dbgval)"
    if($security_software_filenames.Contains($subiefocname)){
        if((Get-ItemProperty ($subiefo).PSPath).PSobject.Properties.name -match "Debugger"){
            Add-SHRTLog "Found bad IEFO: $subiefoname ($dbgval)" -Debug
            Remove-ItemProperty -Path ($subiefo).PSPath -Name "Debugger"
            Add-SHRTLog "Unblocked $subiefocname"
        }
    }
    
}

$disallowrun_path = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
$disallowrun = (Get-ItemProperty $disallowrun_path)
foreach($subprop in $disallowrun){
    $dar = ""
    $darname = ""
    foreach($p in $subprop.PSObject.Properties){
        $darname = $p.Name
        if($darname.StartsWith("PS")){
            Add-SHRTLog "Ignored"
            continue
        }
        else{
            $dar = $p.Value
        }
    }
    Add-SHRTLog "Disallow run entry: $dar $darname" -Debug
    if($security_software_filenames.Contains($dar)){
        Remove-ItemProperty -Path $disallowrun_path -Name $darname
        Add-SHRTLog "Unblocked $dar"
    }
}


Add-SHRTLog "Checking for damaged system files"
New-Item "$env:windir\WinSxS\Temp\PendingDeletes" -ItemType Directory -Force
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow

# TODO: test to make sure this doesn't cause problems
# https://forums.malwarebytes.com/topic/301209-cant-install-malwarebytes-my-pc-is-infected/?do=findComment&comment=1583160
#attrib.exe -s -h "C:\Program Files\Malwarebytes" /s /d
#takeown.exe /f "C:\Program Files\Malwarebytes\" /A /r /d y
#icacls.exe "C:\ProgramData\Malwarebytes\" /reset /T /C /L
#takeown.exe /f "C:\Program Files (x86)\Kaspersky Lab\" /A /r /d y

Write-Host "Repairing Windows Defender"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableRoutinelyTakingAction"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows Defender\Real-Time Protection" -Name "DisableRealtimeMonitoring"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"
# https://forums.malwarebytes.com/topic/301140-pupadwareheuristic-wont-quarantine/#comment-1582969
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableRoutinelyTakingAction"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" -Name "DisableBehaviorMonitoring"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" -Name "DisableOnAccessProtection"
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" -Name "DisableScanOnRealtimeEnable"
# 
Remove-SHRTItemProp -Path "HKLM:\SOFTWARE\Microsoft\Windows Defender Security Center\Notifications" -Name "DisableNotifications"

Set-Service WinDefend -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service Bits -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service trustedinstaller -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service winmgmt -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service EventLog -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service bits
Start-Service WinDefend -ErrorAction SilentlyContinue

$defender_exc_paths = (Get-Mppreference).ExclusionPath
foreach($expath in $defender_exc_paths){
    Add-SHRTLog "Removed exclusion for $expath"
    Remove-MpPreference -ExclusionPath $expath
}
$defender_exc_ext = (Get-Mppreference).ExclusionExtension
foreach($ext in $defender_exc_ext){
    Add-SHRTLog "Removed exclusion for $ext"
    Remove-MpPreference -ExclusionExtension $ext
}
$defender_exc_proc = (Get-Mppreference).ExclusionProcess
foreach($proc in $defender_exc_proc){
    Add-SHRTLog "Removed exclusion for $proc"
    Remove-MpPreference -ExclusionProcess $proc
}
Set-MpPreference -DisableArchiveScanning $false -Force
Set-MpPreference -PUAProtection 1
Set-MpPreference -UILockdown $false
Set-MpPreference -DisableAutoExclusions $true

Update-MpSignature
Start-MpScan -ScanType QuickScan
Remove-MpThreat

Add-SHRTLog "Turning on Windows Firewall"
Set-Service BFE -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service mpsdrv -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service mpssvc -StartupType Automatic -ErrorAction SilentlyContinue
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

Add-SHRTLog "Removing unwanted browser changes"
$chromepol = (Get-ItemProperty "HKCU:\Software\Policies\Google\chrome" -ErrorAction SilentlyContinue | Format-List | Out-String)
Add-SHRTLog "Chrome policies:`n$chromepol" -Debug
Remove-SHRTItemProp -Path "HKCU:\Software\Policies\Google\chrome" -Name "DownloadRestrictions"
Remove-SHRTItemProp -Path "HKCU:\Software\Policies\Microsoft\Edge" -Name "DownloadRestrictions"
Remove-SHRTItemProp -Path "HKCU:\SOFTWARE\Policies\Microsoft\Edge" -Name "HomepageLocation" -ErrorAction SilentlyContinue # https://learn.microsoft.com/en-us/DeployEdge/microsoft-edge-policies#homepagelocation

Add-SHRTLog "Checking for known malware"
$sality1 = (Test-Path "HKCU:\SOFTWARE\zrfke")
if($sality1){
    Add-SHRTLog "Warning: Sality detected! It is recommended you reinstall Windows"
}

Add-SHRTLog "Removing known malware"
Remove-Item "$env:systemdrive\Windows\Fonts\*" -Include "*.exe"
Remove-Item "$env:public\AccountPictures\*" -Include "*.exe"
Remove-Item "$env:localappdata\Microsoft\Windows\PowerShell" -Include "*.vbs"
Remove-Item "HKCU:\Software\Conduit" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\Software\Wow6432Node\Conduit" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKCU:\Software\360Chrome" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKCU:\di" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKCU:\Software\Lavasoft\Web Companion" -Force -ErrorAction SilentlyContinue
Remove-Item "HKCU:\SOFTWARE\zrfke" -Recurse -Force -ErrorAction SilentlyContinue
#  https://forums.malwarebytes.com/topic/301140-pupadwareheuristic-wont-quarantine/#comment-1582969
Remove-Item -Path "HKCU:\SOFTWARE\353526A37049C6636D28F632A766CA4B" -force -ErrorAction SilentlyContinue
Remove-Item -Path "HKCU:\SOFTWARE\4F905DFBB0C92199DB550940702AF609" -force -ErrorAction SilentlyContinue
# https://forums.malwarebytes.com/topic/303905-a-running-process-on-your-device-is-potentially-malicious/
Remove-Item -Path "HKLM:\SOFTWARE\7-ZipAA8xK7ht" -Force -ErrorAction SilentlyContinue
# https://forums.malwarebytes.com/topic/306187-i-have-a-trojan-labeled-trojancryptgeneric-cpu-temp-and-usage-is-up/
Remove-Item -Path "HKLM:\SYSTEM\CURRENTCONTROLSET\SERVICES\GoogleUpdateTaskMachineWI" -Force -ErrorAction SilentlyContinue

# https://stackoverflow.com/questions/69518375/delete-a-locked-file-using-powershell
$Win32 = Add-Type -Passthru -Name Win32 -MemberDefinition '
[DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Auto)]
public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, int dwFlags);'

foreach($malware in $knownmalware){
    if(Test-Path "$malware"){
        try{
            Remove-Item "$malware"
            Add-SHRTLog "Removed $malware"
        }
        catch{
            $Win32::MoveFileEx($malware, [NullString]::Value, 4 <# DelayUntilReboot #> )
            Add-SHRTLog "Reboot to remove $malware"
        }
        
    }
}
foreach($malware in $knownmalwaredirs){
    if(Test-Path "$malware"){
        Remove-Item -Recurse -Force "$malware"
        Add-SHRTLog "Removed $malware"
    }
}

Add-SHRTLog "Checking roots" -Debug
$cleanroots = @("$env:userprofile\AppData\Roaming\Microsoft", "$env:userprofile\AppData\Roaming\Microsoft\Windows", "$env:appdata", "$env:localappdata")
foreach($rapath in $cleanroots){
    Add-SHRTLog "Checking files in $rapath" -Debug
    $roamingmicrosoft = Get-ChildItem $rapath
    foreach($file in $roamingmicrosoft){
        $fname = $file.Name
        Add-SHRTLog "Checking $fname" -Debug
        if($fname.EndsWith(".exe") -or $fname.EndsWith(".scr")){
            $file | Remove-Item 
            Add-SHRTLog "Removed $rapath\$fname"
        }
    }
}

# while this may appear to remove legitimate Google Chrome tasks, all legitimate Chrome tasks should start with Google, ie
# 08/03/2023  01:44 PM             3,666 GoogleUpdateTaskMachineCore{3C3D51F0-3550-4F05-9038-3B7773729F72}
# 08/03/2023  01:44 PM             3,790 GoogleUpdateTaskMachineUA{DAFD2719-AC4D-4124-9A28-DECE3E1533CC}
$all_tasks = (Get-ScheduledTask)
foreach($task in $all_tasks){
    $taskname = $task.taskname
    $taskpath = $task.TaskPath
    $taskfullname = "$taskpath$taskname"
    Add-SHRTLog "Checking $taskfullname" -Debug
    if($taskname.ToLower().StartsWith("chrome")){
        Unregister-ScheduledTask "$taskname" -TaskPath $taskpath -Confirm:$false
        Add-SHRTLog "Removed $taskname"
    }
    if($bad_schtasks.Contains($taskname) -or $bad_schtasks.Contains($taskfullname)){
        Unregister-ScheduledTask "$taskname" -TaskPath $taskpath -Confirm:$false
        Add-SHRTLog "Removed $taskname"
    }
}
$chrome_tasks_files = (Get-ChildItem $env:windir\System32\tasks\* -Recurse -Include "chrome*")
foreach($task in $chrome_tasks_files){
    $taskpath = $task.VersionInfo.FileName
    Remove-Item $taskpath
    Add-SHRTLog "Removed $taskpath"
}

$known_bad_runkeys = @("WindowsSecurity", "gieruwgew", "519b55464950ce55b68715cb59bcfbfb", "WindowsBootManager", "Digital Pulse", "DigitalPulse", "DriverUpdUI.exe", "757D9DEAA02700C32F987B29023E43D7", "9A600B72591E9AC18743731A7139BD9D", "Dtyywptpe", "Windows Updates Service")
$runkeys = @("HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce", "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
foreach($runkey in $runkeys){
    $runv = (Get-ItemProperty $runkey -ErrorAction SilentlyContinue | Format-List | Out-String)
    Add-SHRTLog $runv -Debug
    foreach($bad in $known_bad_runkeys){
        try{
            $bv = Get-ItemProperty -Path $runkey -Name $bad -ErrorAction SilentlyContinue
        }
        catch{

        }
        if($bv){
            Remove-SHRTItemProp -Path "$runkey" -Name "$bad"
            Add-SHRTLog "Removed $runkey|$bad"
        }

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
Remove-Item -Path "HKLM:\SOFTWARE\WOW6432Node\Policies\Microsoft\Windows\WindowsUpdate" -Recurse -Force
Remove-Item -Path HKCU:\SOFTWARE\Classes\.exe
Remove-Item -Path HKCU:\SOFTWARE\Classes\.reg
Remove-Item -Path HKCU:\SOFTWARE\Classes\.bat
bcdedit.exe /set "{default}" recoveryenabled yes
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SafeBoot" -Name "AlternateShell" -Value "cmd.exe"
Remove-SHRTItemProp -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "DisableTaskMgr"
Remove-SHRTItemProp -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "DisableRegistryTools"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "PromptOnSecureDesktop" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorUser" -Value 3
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 3

Add-SHRTLog "Resetting network settings"
NETSH winsock reset catalog
NETSH int ipv4 reset reset.log
NETSH int ipv6 reset reset.log
netsh int ip reset
netsh winsock reset
netsh winhttp reset proxy
ipconfig /flushdns

Add-SHRTLog "Clearing temp files"
bitsadmin /reset /allusers | Out-Null
$tempfolders = @("$env:userprofile\APPDATA\LOCAL\MICROSOFT\WINDOWS\INETCACHE\IE\", "$env:temp", "$env:appdata\Microsoft\Windows\Recent", "$env:systemdrive\Windows\Temp")
foreach($temploc in $tempfolders){
    Get-ChildItem $temploc -Exclude "system_hijack_removal_tool.ps1" | Remove-Item -Recurse -Force
    Add-SHRTLog "Cleared $temploc"
}
Remove-Item "$env:systemdrive\Windows\Prefetch\*" -Include "*.pf"
Remove-Item "$env:windir\SoftwareDistribution\Download\*" -Recurse -Force
Clear-RecycleBin -Force

$twdirs = Get-ChildItem C:\Windows\System32\config\systemprofile\AppData\Local -Directory -Filter "tw-*.tmp"
foreach($dir in $twdirs) {
    if(!(Get-ChildItem $dir.FullName)){
        Remove-Item -Force $dir.FullName
    }
}

Write-Host "You need to reboot your system"
Read-Host "Press enter to end" | Out-Null
