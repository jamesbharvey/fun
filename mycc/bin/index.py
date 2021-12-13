#!/usr/bin/env python
import os
import warnings
import zipfile
import glob
import subprocess
import xml.etree.ElementTree
import pymongo
from pathlib import Path


def xml_tree_to_dictionary(out_dict, xml_path):
    xml_path = os.path.basename(xml_path)
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    if root.tag != 'ComicInfo':
        warnings.warn("tried to parse xml file[" + xml_path + "] that is not ComicInfo")
    for child in root:
        out_dict[child.tag] = child.text
    return out_dict


def set_non_xml_fields_for_dict_to_index(to_index, file_path):
    to_index['FileName'] = os.path.basename(file_path)
    to_index['RelativeFilePath'] = file_path
    to_index['AbsoluteFilePath'] = os.path.abspath(file_path)
    return to_index


def get_dict_to_index_from_zip_file(zip_file_name):
    dict_to_index = {}
    with zipfile.ZipFile(zip_file_name, "r") as zfile:
        xml_file_names = list(filter(lambda x: x.lower().endswith('.xml'), zfile.namelist()))
        if len(xml_file_names) != 1 and len(xml_file_names) != 0:
            warnings.warn("multiple xml files in .cbr[" + zip_file_name + "]....")
            for filename in xml_file_names:
                warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
        for xml_file_name in xml_file_names:
            xml_path = zfile.extract(xml_file_name)
            dict_to_index = xml_tree_to_dictionary(dict_to_index, xml_path)
        return set_non_xml_fields_for_dict_to_index(dict_to_index, zip_file_name)


def get_dict_to_index_from_rar_file(rar_file_name):
    out_dict = {}
    set_non_xml_fields_for_dict_to_index(out_dict, rar_file_name)
    completed_process = subprocess.run(["unrar", "lb", rar_file_name], capture_output=True)
    if completed_process.returncode != 0:
        warnings.warn("couldn't list contents of rarfile[" + rar_file_name + "]")
        return out_dict
    strings = []
    for bytes in completed_process.stdout.splitlines():
        strings.append(str(bytes).rstrip('/n').lstrip("b'").rstrip("'"))
    xml_file_names = list(filter(lambda x: x.lower().endswith('.xml'), strings))
    if len(xml_file_names) != 1 and len(xml_file_names) != 0:
        warnings.warn("multiple xml files in .cbr[" + rar_file_name + "]....")
        for filename in xml_file_names:
            warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
    for xml_file_name in xml_file_names:
        completed_process = subprocess.run(["unrar",
                                            "e",
                                            "-o+",
                                            "-y",
                                            "-inul",
                                            rar_file_name,
                                            xml_file_name])
        if completed_process.returncode != 0:
            warnings.warn("couldn't extract file[" + xml_file_name + "] from rar archive[" + rar_file_name + "]")
            return []
        out_dict = xml_tree_to_dictionary(out_dict, xml_file_name)
    return out_dict


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


def insert_comic(dict_to_index):
    mongoCollection.insert_one(dict_to_index)


def index_directory(directory):
    old_dir = os.getcwd()
    os.chdir(directory)

    if os.path.exists("mycc.indexed"):
        warnings.warn(
            "Directory [" + directory + "] already indexed. To re-index it remove the file mycc.indexed from the "
            + "directory and run again.")
        return

    for file_name in glob.glob('*.[Cc][Bb][Zz]'):
        print(file_name)
        dict_to_index = get_dict_to_index_from_zip_file(file_name)
        print(dict_to_index)
        insert_comic(dict_to_index)

    for file_name in glob.glob('*.[Cc][Bb][Rr]'):
        print(file_name)
        dict_to_index = get_dict_to_index_from_rar_file(file_name)
        print(dict_to_index)
        insert_comic(dict_to_index)

    for item in glob.glob('*'):
        if os.path.isdir(item):
            index_directory(item)

    Path('mycc.indexed').touch()
    os.chdir(old_dir)


directories = [
    '/Users/james.harvey/Desktop/2021.04.21 Weekly Pack',
    '/Users/james.harvey/Desktop/House of M TPBs (2006-2016)',
    '/Users/james.harvey/Desktop/2021.09.29 Weekly Pack',
]

for directory in directories:
    index_directory(directory)
