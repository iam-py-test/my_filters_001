Write-Host "Security Software Unblock Tool"
$security_software_filenames = @("mbam.exe", "msert.exe", "taskmgr.exe", "eav_trial_rus.exe", "eis_trial_rus.exe", "essf_trial_rus.exe", "hitmanpro_x64.exe", "ESETOnlineScanner_UKR.exe", "ESETOnlineScanner_RUS.exe", "HitmanPro.exe", "Cezurity_Scanner_Pro_Free.exe", "Cube.exe", "AVbr.exe", "AV_br.exe", "KVRT.exe", "cureit.exe", "FRST64.exe", "eset_internet_security_live_installer.exe", "esetonlinescanner.exe", "eset_nod32_antivirus_live_installer.exe", "PANDAFREEAV.exe", "bitdefender_avfree.exe", "drweb-12.0-ss-win.exe", "Cureit.exe", "TDSSKiller.exe", "KVRT(1).exe", "rkill.exe", "adwcleaner.exe", "frst.exe", "frstenglish.exe", "combofix.exe", "iexplore.exe", "msconfig.exe", "jrt.exe", "mbar.exe", "SecHealthUI.exe")
$procs_to_kill = @("sOFvE.exe", "aspnet_compiler.exe", "ZBrWfxmlCHpYeX.exe", "n2770812.exe", "legola.exe", "pdates.exe")
$locs_to_kill = @("$env:APPDATA", "$env:TEMP")

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
    $rootdir = Split-Path ($procpath)
    if($locs_to_kill.Contains($rootdir)){
        $proc.kill()
        Write-Host "Killed $procpath"
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
Add-MpPreference -DisableArchiveScanning False
Add-MpPreference -PUAProtection 1
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTOFFERTHROUGHWUAU"
Remove-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432NODE\POLICIES\MICROSOFT\MRT" -Name "DONTREPORTINFECTIONINFORMATION"

Set-Service WinDefend -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service Bits -StartupType Automatic -ErrorAction SilentlyContinue

Start-Service WinDefend -ErrorAction SilentlyContinue

Write-Host "Removing known malware"
Remove-Item C:\Windows\Fonts\* -Include "*.exe"
$knownmalware = @("c:\Users\$env:username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\eNXtBTKShU.url", "c:\Users\Public\Viyeinmz.url", "c:\Users\Public\Owhgjnta.url")
foreach($malware in $knownmalware){
    if(Test-Path "$malware"){
        Remove-Item "$malware"
        Write-Host "Removed $malware"
    }
}

Write-Host "Clearing temp files..."
$tempfolders = @("C:\USERS\$env:username\APPDATA\LOCAL\MICROSOFT\WINDOWS\INETCACHE\IE\", "$env:temp", "$env:appdata\Microsoft\Windows\Recent", "C:\Windows\Temp")
foreach($temploc in $tempfolders){
    Get-ChildItem $temploc | Remove-Item -Recurse -Force
    Write-Host "Cleared $temploc"
}
Remove-Item "C:\Windows\Prefetch\*" -Include "*.pf"

Write-Host "You need to reboot your system"
Read-Host "Press enter to end" | Out-Null
