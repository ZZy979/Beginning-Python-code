$Url = "https://repo1.maven.org/maven2/org/python/jython-installer/2.7.3/jython-installer-2.7.3.jar"
$JarFile = "jython-installer-2.7.3.jar"
$InstallDir = "$HOME\jython"

Set-Location -Path $env:TMP
Invoke-WebRequest -Uri $Url -OutFile $JarFile
java -jar $JarFile -s -d $InstallDir -t minimum
Remove-Item $JarFile
