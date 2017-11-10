from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

from .models import Movies


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print("inside homepage")
    context = {'movie_list': Movies.objects.all()}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def mainboard(request):
    print("inside mainboard")
    wishmovie = request.GET.get('movie', None)
    print(wishmovie)
    context = {'movie_list': Movies.objects.all()}
    data = {
        'exists': False
    }
    return JsonResponse(data)
    return render(request, 'polls/details.html', context)

def insert_wishlist(request):
    print("something for debug")
    print(request)
    wishmovie = request.GET.get('movie', None)
    console.log(wishmovie)
    data = {
        'exists': False
    }
    return JsonResponse(data)
