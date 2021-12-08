#!/usr/bin/env python
import os
import warnings
import zipfile
import glob
import subprocess
import xml.etree.ElementTree as ET

def xmlTreeToDictionary(dict,xmlpath):
    xmlpath = os.path.basename(xmlpath)
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    if root.tag != 'ComicInfo':
        warnings.warn("tried to parse xml file[" + xmlpath + "] that is not ComicInfo")
    for child in root:
        dict[child.tag] = child.text
    return dict

def setNonXmlFieldsForDictToIndex(dictToIndex,filepath):
    dictToIndex['FileName'] = os.path.basename(filepath)
    dictToIndex['OsFilePath'] = filepath
    return dictToIndex

def getDictToIndexFromZipFile(zipfilename):
    dictToIndex = {}
    with zipfile.ZipFile(filename, "r") as zfile:
        xmlfilenames = list(filter(lambda x: x.lower().endswith('.xml'), zfile.namelist()))
        if len(xmlfilenames) != 1 and len(xmlfilenames) != 0:
            warnings.warn("multiple xml files in .cbr[" + zipfilename + "]....")
        for xmlfilename in xmlfilenames:
            xmlpath = zfile.extract(xmlfilename)
            dictToIndex = xmlTreeToDictionary(dictToIndex, xmlpath)
        return setNonXmlFieldsForDictToIndex(dictToIndex, zipfilename)

def getDictToIndexFromRarFile(rarfilename):
    dict = {}
    setNonXmlFieldsForDictToIndex(dict, rarfilename)
    completedProcess = subprocess.run(["unrar", "lb", rarfilename], capture_output=True)
    if completedProcess.returncode != 0:
        warnings.warn("couldn't list contents of rarfile[" + rarfilename + "]")
        return dict
    strings = []
    for bytes in completedProcess.stdout.splitlines():
        strings.append(str(bytes).rstrip('/n').lstrip("b'").rstrip("'"))
    xmlfilenames = list(filter(lambda x: x.lower().endswith('.xml'), strings))
    if len(xmlfilenames) != 1 and len(xmlfilenames) != 0:
        warnings.warn("multiple xml files in .cbr[" + rarfilename + "]....")
        for filename in xmlfilenames:
            warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
    for xmlfilename in xmlfilenames:
        completedProcess = subprocess.run(["unrar",
                                           "e",
                                           "-o+",
                                           "-y",
                                           "-inul",
                                           rarfilename,
                                           xmlfilename])
        if completedProcess.returncode != 0:
            warnings.warn("couldn't extract file[" + xmlfilename + "] from rar archive[" + rarfilename + "]")
            return []
        dict = xmlTreeToDictionary(dict,xmlfilename)
    return dict

os.chdir('/Users/james.harvey/Desktop/2021.04.21 Weekly Pack')

for filename in glob.glob('*/*.[Cc][Bb][Zz]'):
    print(filename)
    dictToIndex = getDictToIndexFromZipFile(filename)
    print(dictToIndex)

for filename in glob.glob('*/*.[Cc][Bb][Rr]'):
    print(filename)
    dictToIndex = getDictToIndexFromRarFile(filename)
    print(dictToIndex)