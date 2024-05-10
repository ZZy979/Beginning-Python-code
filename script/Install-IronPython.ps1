$Url = "https://github.com/IronLanguages/ironpython3/releases/download/v3.4.1/IronPython.3.4.1.zip"
$ZipFile = "IronPython.3.4.1.zip"
$InstallDir = "$HOME\IronPython"

Set-Location -Path $env:TMP
Invoke-WebRequest -Uri $Url -OutFile $ZipFile
Expand-Archive -Path $ZipFile -DestinationPath $InstallDir
Remove-Item $ZipFile
