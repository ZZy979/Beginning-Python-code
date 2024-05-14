#!/bin/bash

url="https://repo1.maven.org/maven2/org/python/jython-installer/2.7.3/jython-installer-2.7.3.jar"
jar_file=jython-installer-2.7.3.jar
install_dir=$HOME/jython

cd /tmp
wget $url
java -jar $jar_file -s -d $install_dir -t minimum
rm $jar_file
