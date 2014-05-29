#!/bin/sh

export JAVA_HOME=/usr

git clone git://libvirt.org/libvirt-python.git
git clone git://libvirt.org/libvirt-java.git

cp pom.xml.libvirt-java libvirt-java/pom.xml
mvn clean install


