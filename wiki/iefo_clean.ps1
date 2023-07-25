Write-Host Image File Execution Options cleaner
$worryingiefo = @("mbam.exe", "msert.exe", "taskmgr.exe")
$iefo = (Get-ChildItem "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options")
foreach($subiefo in $iefo){
    $dbgval = (Get-ItemProperty ($subiefo).PSPath).Debugger
    $subiefoname = $subiefo.Name
    $subiefocname = $subiefo.PSChildName
    if($worryingiefo.Contains($subiefocname)){
        if((Get-ItemProperty ($subiefo).PSPath).PSobject.Properties.name -match "Debugger"){
             Remove-ItemProperty -Path ($subiefo).PSPath -Name "Debugger"
             Write-Host "Unblocked $subiefocname"
        }
    }
    
}
