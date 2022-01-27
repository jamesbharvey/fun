#!/usr/bin/env python
import os
import re
import warnings
import zipfile
import glob
import subprocess
import xml.etree.ElementTree
import pymongo
from PyPDF4 import PdfFileReader
from pathlib import Path


class ComicFileHandler:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.to_index = {}

    def parse_and_set_xml_fields(self, xml_path):
        xml_path = os.path.basename(xml_path)
        tree = xml.etree.ElementTree.parse(xml_path)
        root = tree.getroot()
        if root.tag != 'ComicInfo':
            warnings.warn("tried to parse xml file[" + xml_path + "] that is not ComicInfo")
            return
        for child in root:
            self.to_index[child.tag] = child.text

    def set_download_type(self):
        match = re.search('\d{4}\.\d{1,2}\.\d{1,2} Weekly Pack', self.to_index['AbsoluteFilePath'])
        if match is not None:
            self.to_index['DownloadType'] = 'Weekly'
            return
        file_directory = self.to_index['AbsoluteFilePath']
        file_directory = file_directory.removesuffix(self.to_index['FileName'])
        file_directory = file_directory.removesuffix('/')
        if file_directory not in directories:
            self.to_index['DownloadType'] = 'Collection'
            return
        self.to_index['DownloadType'] = 'Single'
        return

    def set_non_xml_fields(self):
        self.to_index['FileName'] = os.path.basename(self.archive_path)
        self.to_index['RelativeFilePath'] = self.archive_path
        self.to_index['AbsoluteFilePath'] = os.path.abspath(self.archive_path)
        self.set_download_type()

    def parse_file(self):
        archive_path_str = str(self.archive_path)
        if archive_path_str.lower().endswith('.cbz'):
            self.parse_zip_file()
        if archive_path_str.lower().endswith('.cbr'):
            self.parse_rar_file()
        if archive_path_str.lower().endswith('.pdf'):
            self.parse_pdf_file()

    def set_format(self, page_count):
        if 'Series' in self.to_index and 'Number' in self.to_index:
            self.to_index['Format'] = 'Floppy'
            return
        # yes this is crude and will not work for Euro Comics, etc.
        # picked 82 for 80-page giants + cover + "scanned by" page
        if 'PageCount' in self.to_index:
            page_count = int(self.to_index['PageCount'])
        if page_count > 82:
            self.to_index['Format'] = 'Trade'
        else:
            self.to_index['Format'] = 'Floppy'

    def parse_zip_file(self):
        try:
            with zipfile.ZipFile(self.archive_path, "r") as zfile:
                page_count = len(list(filter(lambda x: x.lower().endswith('.jpg'), zfile.namelist())))
                self.set_format(page_count)
                xml_file_names = list(filter(lambda x: x.lower().endswith('.xml'), zfile.namelist()))
                if len(xml_file_names) != 1 and len(xml_file_names) != 0:
                    warnings.warn("multiple xml files in .cbr[" + self.archive_path + "]....")
                    for filename in xml_file_names:
                        warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
                for xml_file_name in xml_file_names:
                    xml_path = zfile.extract(xml_file_name)
                    self.parse_and_set_xml_fields(xml_path)
                self.set_format(page_count)
        except (IOError, zipfile.BadZipfile) as e:
            warnings.warn("BadZipFile exception for file:" + self.archive_path)
        self.set_non_xml_fields()

    def parse_rar_file(self):
        self.set_non_xml_fields()
        completed_process = subprocess.run(["unrar", "lb", self.archive_path], capture_output=True)
        if completed_process.returncode != 0:
            warnings.warn("couldn't list contents of rarfile[" + self.archive_path + "]")
            return
        strings = []
        for bytes in completed_process.stdout.splitlines():
            strings.append(str(bytes).rstrip('/n').lstrip("b'").rstrip("'"))
        page_count = len(list(filter(lambda x: x.lower().endswith('.jpg'), strings)))
        xml_file_names = list(filter(lambda x: x.lower().endswith('.xml'), strings))
        if len(xml_file_names) != 1 and len(xml_file_names) != 0:
            warnings.warn("multiple xml files in .cbr[" + self.archive_path + "]....")
            for filename in xml_file_names:
                warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
        # there are several rar libraries in python but none
        # of them are reliable enough or support enough features to unrar
        # files from the wild reliably, so we use the official free-as-in-beer version
        # which must be installed on your path
        for xml_file_name in xml_file_names:
            completed_process = subprocess.run(["unrar",
                                                "e",
                                                "-o+",
                                                "-y",
                                                "-inul",
                                                self.archive_path,
                                                xml_file_name])
            if completed_process.returncode != 0:
                warnings.warn("couldn't extract file[" + xml_file_name +
                              "] from rar archive[" + self.archive_path + "]")
                return []
            self.parse_and_set_xml_fields(xml_file_name)
        self.set_format(page_count)

    def parse_pdf_file(self):
        self.set_non_xml_fields()
        with open(self.archive_path, 'rb') as f:
            pdf = PdfFileReader(f)
            doc_info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            self.to_index['Writer'] = doc_info.author
            self.to_index['Title'] = doc_info.title
            self.to_index['PageCount'] = number_of_pages
            self.set_format(number_of_pages)


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
        os.chdir(old_dir)
        return
    file_names = glob.glob('*.[Cc][Bb][ZzRr]')
    for file_name in glob.glob('*.[pP][Dd][fF]'):
        file_names.append(file_name)
        print(file_name)
    for file_name in file_names:
        print(os.path.abspath(file_name))
        fp = ComicFileHandler(file_name)
        fp.parse_file()
        insert_comic(fp.to_index)
    for zip_collection in glob.glob('*.[zZ][iI][pP]'):
        zfile = zipfile.ZipFile(zip_collection, "r")
        pre_unzip_dir = os.getcwd()
        dir_for_unzip = zip_collection.removesuffix('.zip')
        if not os.path.isdir(dir_for_unzip):
            os.mkdir(dir_for_unzip)
        os.chdir(dir_for_unzip)
        zfile.extractall()
        zfile.close
        os.chdir(pre_unzip_dir)
    home_dir = os.environ.get("HOME")
    completed_process = subprocess.run([home_dir + "/fun/bin/cbthumb"], capture_output=True)
    if completed_process.returncode != 0:
        warnings.warn("failed to run cbthumb in directory[" + os.getcwd() + "]")
    for item in glob.glob('*'):
        if os.path.isdir(item):
            index_directory(item)
    Path('mycc.indexed').touch()
    os.chdir(old_dir)


directories = [
'/mnt/buffalo2tb/done',
'/home/james/broken',
]

for directory in directories:
    if os.path.exists(directory):
        index_directory(directory)

