from django.http import HttpResponse
from django.shortcuts import loader

def index(request):
    template = loader.get_template('search/index.html')
    context = {
        'latest_question_list': '',
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
