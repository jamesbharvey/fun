#!/usr/bin/env python
import warnings
import zipfile
import glob
import subprocess

def getXmlFilesFromZipFile(zfile):
    xmlfilenames = list(filter(lambda x: x.lower().endswith('.xml'), zfile.namelist()))
    for xmlfilename in xmlfilenames:
        xmlpath = zfile.extract(xmlfilename)
        xmlfile = open(xmlpath)
        #print(xmlfile.readlines())
        xmlfile.close()
    return xmlfilenames

def getXmlFilesFromRarFile(rfilename):
    completedProcess = subprocess.run(["unrar", "lb", rfilename], capture_output=True)
    if completedProcess.returncode != 0:
        return []
    strings = []
    for bytes in completedProcess.stdout.splitlines():
        strings.append(str(bytes).rstrip('/n').lstrip("b'").rstrip("'"))
    xmlfilenames = list(filter(lambda x: x.lower().endswith('.xml'), strings))
    for xmlfilename in xmlfilenames:
        print (rfilename + " : " + xmlfilename)
        completedProcess = subprocess.run(["unrar",
                                          "e",
                                          "-o+",
                                          "-y",
                                          "-inul",
                                          rfilename,
                                          xmlfilename])
        if completedProcess.returncode != 0:
            warnings.warn("couldn't extract file[" + xmlfile + "] from rar archive[" + rfilename + "]")
            return []
        xmlfile = open(xmlfilename)
        print(xmlfile.readlines())
        xmlfile.close()
    return xmlfilenames


for filename in glob.glob('*.[Cc][Bb][Zz]'):
    zfile = zipfile.ZipFile(filename, "r")
    xmlfilenames = getXmlFilesFromZipFile(zfile)

for filename in glob.glob('*.[Cc][Bb][Rr]'):
    xmlfilenames = getXmlFilesFromRarFile(filename)
    print(xmlfilenames)



exit()

# list file information
# for info in file.infolist():
#    print info.filename, info.date_time, info.file_size
