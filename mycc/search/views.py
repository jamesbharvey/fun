from django.http import HttpResponse
from django.shortcuts import loader
import pymongo
import urllib.parse

mongoClient = pymongo.MongoClient()
mongoDbName = mongoClient['mycc']
mongoCollection = mongoDbName['comics']


def index(request):
    template = loader.get_template('search/index.html')
    comicList = []
    context = {'keywords': ''}
    getParams = request.GET.dict()
    if 'keywords' in getParams:
        context['keywords'] = getParams['keywords']
        query = {"$text": {"$search": getParams['keywords']}}
        cursor = mongoCollection.find(query)
        absolutePathRoots = [["/Users/james.harvey/Desktop/", "http://127.0.0.1:8080/"]]
        for comic in cursor:
            absoluteFilePath = str(comic['AbsoluteFilePath'])
            for pathUrlTuple in absolutePathRoots:
                rootRelativePath = absoluteFilePath.lstrip(pathUrlTuple[0])
            comic['url'] = pathUrlTuple[1] + urllib.parse.quote(rootRelativePath)
            comicList.append(comic)
    numComics = len(comicList)

    context['comics'] = comicList
    context['numComics'] = numComics
    return HttpResponse(template.render(context, request))

# Create your views here.
