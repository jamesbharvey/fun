from django.http import HttpResponse
from django.shortcuts import loader
import pymongo
import urllib.parse

from pymongo import MongoClient

mongo_client: MongoClient = pymongo.MongoClient()
mongo_db_name = mongo_client['mycc']
mongo_collection = mongo_db_name['comics']


def index(request):
    template = loader.get_template('search/index.html')
    comic_list = []
    context = {'keywords': ''}
    get_params = request.GET.dict()
    if 'keywords' in get_params:
        context['keywords'] = get_params['keywords']
        query = {"$text": {"$search": get_params['keywords']}}
        cursor = mongo_collection.find(query)
        absolute_path_roots = [["/Users/james.harvey/Desktop/", "http://127.0.0.1:8080/"]]
        for comic in cursor:
            fields_for_link_title = []
            for field in (
                          'Series',
                          'Number',
                          'Title',
                          'Writer',
                          'Penciller',
                          'Genre',
                          'Publisher',
                          'Format',
                          'Summary',
                          'FileName'):
                if field in comic:
                    fields_for_link_title.append(field + " : " + str(comic[field]))
            comic['LinkTitle'] = "\n".join(fields_for_link_title)
            absolute_file_path = str(comic['AbsoluteFilePath'])
            for path_url_tuple in absolute_path_roots:
                root_relative_path = absolute_file_path.lstrip(path_url_tuple[0])
            comic['Url'] = path_url_tuple[1] + urllib.parse.quote(root_relative_path)
            comic_list.append(comic)
    num_comics = len(comic_list)
    context['comics'] = comic_list
    context['num_comics'] = num_comics
    return HttpResponse(template.render(context, request))

# Create your views here.
