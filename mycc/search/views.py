from django.http import HttpResponse
from django.shortcuts import loader
import pymongo
import urllib.parse

mongoClient = pymongo.MongoClient()
mongoDbName = mongoClient['mycc']
mongoCollection = mongoDbName['comics']


def index(request):
    template = loader.get_template('search/index.html')
    cursor = mongoCollection.find()
    comicList = []
    for comic in cursor:
        rootRelativePath = str(comic['AbsoluteFilePath']).replace("/Users/james.harvey/Desktop/", "")
        comic['url'] = "http://127.0.0.1:8080/" + urllib.parse.quote(rootRelativePath)
        comicList.append(comic)
    numComics = len(comicList)
    context = {
        'comics': comicList,
        'numComics': numComics
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
