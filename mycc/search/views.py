from django.http import HttpResponse
from django.shortcuts import loader
import pymongo
import urllib.parse

from pymongo import MongoClient

mongo_client: MongoClient = pymongo.MongoClient("mongodb://myccuser:secretpassword@192.168.11.23:27017")
mongo_db_name = mongo_client['mycc']
mongo_collection = mongo_db_name['comics']

from elasticsearch import Elasticsearch

esClient = Elasticsearch("http://192.168.11.23:9200")
esIndexName = ""


def mongo(request):
    template = loader.get_template('search/mongo.html')
    comic_list = []
    context = {'keywords': ''}
    get_params = request.GET.dict()
    if 'format' in get_params:
        context['format'] = get_params['format']
    else:
        context['format'] = 'Any'
    if 'search_mode' in get_params:
        context['search_mode'] = get_params['search_mode']
    else:
        context['search_mode'] = "simple"
    if 'download_type' in get_params:
        context['download_type'] = get_params['download_type']
    else:
        context['download_type'] = 'Any'
    if 'sort_type' in get_params:
        context["sort_type"] = get_params["sort_type"]
    else:
        context["sort_type"] = "Relevance"
    if 'keywords' in get_params:
        context['keywords'] = get_params['keywords']
        cursor = mongo_collection.find({"$text": {"$search": get_params['keywords']}},
                                       {'score': {"$meta": 'textScore'}})
        if context['sort_type'] == "FileName":
            cursor.sort("FileName", pymongo.ASCENDING)
        else:
            cursor.sort([('score', {'$meta': 'textScore'})])
        absolute_path_roots = [
            ["/mnt/", "http://192.168.11.23/"],
            ["/home/james/broken", "http://127.0.0.1/broken/"],
        ]
        for comic in cursor:
            if context['format'] != 'Any':
                if comic["Format"] != context['format']:
                    continue
            if context['download_type'] != 'Any':
                if comic["DownloadType"] != context["download_type"]:
                    continue
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
                    'DownloadType',
                    'Summary',
                    'FileName'):
                if field in comic:
                    fields_for_link_title.append(field + " : " + str(comic[field]))
            comic['LinkTitle'] = "\n".join(fields_for_link_title)
            absolute_file_path = str(comic['AbsoluteFilePath'])
            for path_url_tuple in absolute_path_roots:
                if absolute_file_path.find(path_url_tuple[0]) == 0:
                    root_relative_path = absolute_file_path.replace(path_url_tuple[0], '')
                    comic['Url'] = path_url_tuple[1] + urllib.parse.quote(root_relative_path)
            comic_list.append(comic)
    num_comics = len(comic_list)
    context['comics'] = comic_list
    context['num_comics'] = num_comics
    return HttpResponse(template.render(context, request))


def elastic(request):
    template = loader.get_template('search/elastic.html')
    comic_list = []
    context = {'keywords': ''}
    num_comics = 0
    get_params = request.GET.dict()
    if 'format' in get_params:
        context['format'] = get_params['format']
    else:
        context['format'] = 'Any'
    if 'search_mode' in get_params:
        context['search_mode'] = get_params['search_mode']
    else:
        context['search_mode'] = "simple"
    if 'download_type' in get_params:
        context['download_type'] = get_params['download_type']
    else:
        context['download_type'] = 'Any'
    if 'from' in get_params:
        context['from'] = get_params['from']
    else:
        context['from'] = 0
    if 'size' in get_params:
        context['size'] = get_params['size']
    else:
        context['size'] = 20
    if 'sort_type' in get_params:
        context["sort_type"] = get_params["sort_type"]
    else:
        context["sort_type"] = "Relevance"
    if 'keywords' in get_params:
        context['keywords'] = get_params['keywords']
        query = {
            "from": context['from'],
            "size": context['size'],
            "query": {
                "match": {
                    "FileName": context['keywords']
                }
            }
        }
        response = esClient.search(index="comics", body=query)
        hits = response["hits"]["hits"]
        num_comics = response["hits"]["total"]["value"]

        # cursor = esClient.search({"$text": {"$search": get_params['keywords']}}, {'score': {"$meta": 'textScore'}})
        # if context['sort_type'] == "FileName":
        #    cursor.sort("FileName", pymongo.ASCENDING)
        # else:
        #    cursor.sort([('score', {'$meta': 'textScore'})])
        absolute_path_roots = [
            ["/mnt/", "http://192.168.11.23/"],
            ["/home/james/broken", "http://127.0.0.1/broken/"],
        ]
        for hit in hits:
            comic = hit['_source']
            if context['format'] != 'Any':
                if comic["Format"] != context['format']:
                    continue
            if context['download_type'] != 'Any':
                if comic["DownloadType"] != context["download_type"]:
                    continue
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
                    'DownloadType',
                    'Summary',
                    'FileName'):
                if field in comic:
                    fields_for_link_title.append(field + " : " + str(comic[field]))
            comic['LinkTitle'] = "\n".join(fields_for_link_title)
            absolute_file_path = str(comic['AbsoluteFilePath'])
            for path_url_tuple in absolute_path_roots:
                if absolute_file_path.find(path_url_tuple[0]) == 0:
                    root_relative_path = absolute_file_path.replace(path_url_tuple[0], '')
                    comic['Url'] = path_url_tuple[1] + urllib.parse.quote(root_relative_path)
            comic_list.append(comic)
    context['comics'] = comic_list
    context['num_comics'] = num_comics
    ##
    ## TODO: there must be a simpler way to do this pagination stuff
    ##
    page_from = int(context['from'])
    page_size = int(context['size'])
    if (page_from + page_size) >= num_comics:
        # is last page
        context['next_page_num_results'] = 0
        if (num_comics % page_size) > 0:
            context['this_page_num_results'] = num_comics % page_size
        else:
            context['this_page_num_results'] = page_size
    else:
        # is not last page
        num_results_left = num_comics - (page_from + page_size)
        if num_results_left >= page_size :
            context['next_page_num_results'] = page_size
            context['this_page_num_results'] = page_size
        else:
            last_page_results = num_comics % page_size
            context['next_page_num_results'] = last_page_results
            context['this_page_num_results'] = page_size

    return HttpResponse(template.render(context, request))

# Create your views here.
