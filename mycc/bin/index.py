#!/usr/bin/env python
import os
import warnings
import zipfile
import glob
import subprocess
import xml.etree.ElementTree as ET
import pymongo
from pathlib import Path

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
    dictToIndex['RelativeFilePath'] = filepath
    dictToIndex['AbsoluteFilePath'] = os.path.abspath(filepath)
    return dictToIndex

def getDictToIndexFromZipFile(zipfilename):
    dictToIndex = {}
    with zipfile.ZipFile(zipfilename, "r") as zfile:
        xmlfilenames = list(filter(lambda x: x.lower().endswith('.xml'), zfile.namelist()))
        if len(xmlfilenames) != 1 and len(xmlfilenames) != 0:
            warnings.warn("multiple xml files in .cbr[" + zipfilename + "]....")
            for filename in xmlfilenames:
                warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
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


mongoClient = pymongo.MongoClient()
mongoDbName = mongoClient['mycc']
mongoCollection = mongoDbName['comics']

mongoCollection.create_index([("FileName", "text"),
                              ("Series", "text"),
                              ("Title", "text"),
                              ("Summary", "text"),
                              ("Genre", "text"),
                              ("Writer", "text"),
                              ("Penciller", "text"),
                              ("Year", "text"),
                              ("Number", "text")])

def insertComic(dictToIndex):
    mongoCollection.insert_one(dictToIndex)

def indexDirectory(directory):
    olddir = os.getcwd()
    os.chdir(directory)
    if os.path.exists("mycc.indexed.txt"):
        warnings.warn(
            "Directory [" + directory + "]already indexed. To re-index it remove the file mycc.indexed.txt from the directory and run again.")
        return

    for filename in glob.glob('*.[Cc][Bb][Zz]'):
        print(filename)
        dictToIndex = getDictToIndexFromZipFile(filename)
        print(dictToIndex)
        insertComic(dictToIndex)

    for filename in glob.glob('*.[Cc][Bb][Rr]'):
        print(filename)
        dictToIndex = getDictToIndexFromRarFile(filename)
        print(dictToIndex)
        insertComic(dictToIndex)

    for item in glob.glob('*'):
        if os.path.isdir(item):
            indexDirectory(item)

    Path('mycc.indexed.txt').touch()
    os.chdir(olddir)

directories = [
    '/Users/james.harvey/Desktop/2021.04.21 Weekly Pack',
    '/Users/james.harvey/Desktop/House of M TPBs (2006-2016)',
    '/Users/james.harvey/Desktop/2021.09.29 Weekly Pack',
    ]

for directory in directories:
    indexDirectory(directory)