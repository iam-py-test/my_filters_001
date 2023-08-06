Write-Host "Hidden uninstall entries"
$uninstall_entries = (Get-ChildItem HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall)
foreach($u in $uninstall_entries){
    $uname = $u.Name
    $props = Get-ItemProperty "Registry::$uname"
    if($props.SystemComponent -eq 1){
        Write-Host $props.DisplayName
    }
}

$unhide = (Read-Host "Enter the name of the program to unhide (press enter to unhide nothing)")
if($unhide -eq ""){
    Write-Host "Nothing unhidden"
    exit;
}

$uninstall_entries = (Get-ChildItem HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall)
foreach($u in $uninstall_entries){
    $uname = $u.Name
    $props = Get-ItemProperty "Registry::$uname"
    if($props.DisplayName -eq $unhide){
        $dname = $props.DisplayName
        Write-Host "Unhiding $dname"
        Set-ItemProperty -Path "Registry::$uname" -Name "SystemComponent" -Value 0
    }
}
