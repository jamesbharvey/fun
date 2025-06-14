#!/usr/bin/env python
import os
import re
import warnings
import zipfile
import glob
import subprocess
from defusedxml.ElementTree import parse
import pymongo
import argparse
from PyPDF4 import PdfFileReader
from pathlib import Path
from elasticsearch import Elasticsearch



class ComicFileHandler:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.to_index = {}

    def parse_and_set_xml_fields(self, xml_path):
        try:
            tree = parse(xml_path)
            root = tree.getroot()
            if root.tag != 'ComicInfo':
                warnings.warn("tried to parse xml file[" + xml_path + "] that is not ComicInfo")
                return
            for child in root:
                if child.text is not None:
                    self.to_index[child.tag] = child.text
        except:
            warnings.warn("error parsing xml file [" + xml_path + "] for comic archive file ["
                          + self.archive_path + "]")
            return

    def set_download_type(self):
        match = re.search('\d{4}\.\d{1,2}\.\d{1,2} Weekly Pack', self.to_index['AbsoluteFilePath'])
        if match is not None:
            self.to_index['DownloadType'] = 'Weekly'
            return
        match = re.search('0-Day Week of \d{4}\.\d{1,2}\.\d{1,2}', self.to_index['AbsoluteFilePath'])
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
        # yes this is crude and will not work for Euro Comics, etc.
        # picked 82 for 80-page giants + cover + "scanned by" page
        if 'PageCount' in self.to_index and self.to_index['PageCount'] is not None:
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
                    warnings.warn("multiple xml files in .cbz[" + self.archive_path + "]....")
                    for filename in xml_file_names:
                        warnings.warn("xml file name is [" + filename + "]", stacklevel=1)
                for xml_file_name in xml_file_names:
                    if os.path.exists(xml_file_name):
                        os.remove(xml_file_name)
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
            if os.path.exists(xml_file_name):
                os.remove(xml_file_name)
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
            xml_file_name = os.path.basename(xml_file_name)
            self.parse_and_set_xml_fields(xml_file_name)
        self.set_format(page_count)

    def parse_pdf_file(self):
        self.set_non_xml_fields()
        with open(self.archive_path, 'rb') as f:
            pdf = PdfFileReader(f)
            number_of_pages = pdf.getNumPages()
            self.to_index['PageCount'] = number_of_pages
            self.set_format(number_of_pages)
            doc_info = pdf.getDocumentInfo()
            if doc_info is not None:
                if doc_info.author is not None:
                    self.to_index['Writer'] = doc_info.author
                if doc_info.title is not None:
                    self.to_index['Title'] = doc_info.title


def insert_comic(dict_to_index):
    resp = esClient.index(index=esIndexName, document=dict_to_index)
    mongoCollection.insert_one(dict_to_index)

def index_directory(directory):
    old_dir = os.getcwd()
    os.chdir(directory)
    if os.path.exists("mycc.indexed") and not args.force:
        warnings.warn(
            "Directory [" + directory + "] already indexed. To re-index it remove the file mycc.indexed from the "
            + "directory and run again, or run with --force.")
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
    '/mnt/buffalo2tb/torrents.done',
    '/mnt/buffalo2tb/torrents.done2',
    '/mnt/buffalo2tb/torrents.automoved',
    '/mnt/seagate8tb/torrents.done',
    '/mnt/buffalo8tb/torrents.done',
    '/home/james/broken',
]
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-f", "--force", help="index files regardless",
                    action="store_true")
parser.add_argument("-r", "--refresh", help="delete the existing index and make a new one",
                    action="store_true")
parser.add_argument("-p", "--production", help="use the production collection",
                    action="store_true")
parser.add_argument("-u", "--update", help="check the top level directories for added files",
                    action="store_true")

args = parser.parse_args()

mongoClient = pymongo.MongoClient("mongodb://myccuser:secretpassword@192.168.11.23:27017")
mongoDbName = mongoClient['mycc']

esClient = Elasticsearch("http://192.168.11.23:9200")
esIndexName=""


if args.production:
    mongoCollection = mongoDbName['comics']
    esIndexName = "comics"
else:
    mongoCollection = mongoDbName['test']
    esIndexName = "test1"

if args.refresh:
    mongoCollection.drop()
mongoCollection.create_index([("FileName", "text"),
                              ("Series", "text"),
                              ("Title", "text"),
                              ("Summary", "text"),
                              ("Writer", "text"),
                              ("Year", "text"),
                              ("Number", "text"),
                              ("AbsoluteFilePath", "text")],
                             weights={
                                 'FileName': 10,
                                 'Series': 5,
                                 "Title":1,
                                 "Number": 5,
                                 'Summary': 1,
                                 "Writer": 5,
                                 "Year": 1,
                                 "AbsoluteFilePath": 5,
                             }
                             )

for directory in directories:
    if os.path.exists(directory):
        if args.update:
            os.remove(directory + "/mycc.indexed")
            os.remove(directory + "/index.html")
        index_directory(directory)
