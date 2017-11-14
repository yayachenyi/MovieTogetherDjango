from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Movies, Wish, Users
from .signals import delete_wishlist 

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
    #print(wishmovie)
    context = {'movie_list': Movies.objects.all()}
    data = {
        'exists': False
    }
    JsonResponse(data)
    return render(request, 'polls/details.html', context)

def insertwishlist(request):
    print("something for debug")
    print(request)
    # insert to wisttable , RETURN true/false
    wishmovie = request.GET.get('movie', None)
    userid = request.GET.get('userid', None)
    #console.log(wishmovie)
    print(wishmovie)
    print(userid)
    exist = Wish.objects.filter(userid=userid, movieid=wishmovie)
    if exist:
        data = {
            'exists': True
        }
    else:
        Wish(userid=userid, movieid=wishmovie).save()
        data = {
            'exists': False
        }
    return JsonResponse(data)

def search(request):
    # INPUT : string, part of movie name
    # OUTPUT: table, all the matchrecords
    searchmovie = request.GET.get('qquery', None)
    print(searchmovie)
    if(searchmovie == None):
        searchmovie = "she"
    data = Movies.objects.filter(title__icontains=searchmovie)
    context = {'movie_list': data}
    return render(request, 'polls/search.html', context)

def searchupdate(request):
    # INPUT : string, part of movie name
    # OUTPUT: table, all the matchrecords
    searchmovie = request.GET.get('qquery', None)
    print(searchmovie)
    if(searchmovie == None):
        searchmovie = "she"
    data = Movies.objects.filter(title__icontains=searchmovie)
    print(data)
    context = {'movie_list': data}
    #return render(request, 'polls/search.html', context)
    html = render_to_string('polls/search.html', context)
    return HttpResponse(html)

def wishlist(request):
    # return wishtable
    userid = request.GET.get('userid', None)
    print(userid)
    wishlist = Wish.objects.filter(userid=0).values_list('movieid')
    context = {'movie_list': Movies.objects.filter(movieid__in=wishlist)}
    return render(request, 'polls/wishlist.html', context)

def deletepost(request):
    # perform delete opration
    wishmovie = request.GET.get('movie', None)
    userid = request.GET.get('userid', None)
    exist = Wish.objects.filter(userid=userid, movieid=wishmovie)
    if exist:
        exist.delete()
        delete_wishlist(sender=Wish, instance=exist, user=request.user)
        data = {
            'exists': True
        }
    else:
        data = {
            'exists': False
        }
    return JsonResponse(data)

def profile(request):
    print("insideprofile")
    data = {
          'name' : 'Admin User',
          'gender' : 'female',
          'location' : 'Champaign'
    }
    context = {'user_info' : data}
    return render(request, 'polls/profile.html', context)

def profileupdate(request):
    userid = request.GET.get('userid', None)
    newname = request.GET.get('newname', None)
    newgender = request.GET.get('newgender', None)
    newlocation = request.GET.get('newlocation', None)
    
    # perform user database update here
    # update = Users.objects.get(userid=userid)
    update = Users.objects.get(userid=0)
    if update:
        update.username = newname
        update.gender = newgender
        update.location = newlocation
        update.save()
    else:
        Users(userid=0, username=newname, gender=newgender, location=newlocation).save()
    
    print(newname)
    data = {
          'name' : newname,
          'gender' : newgender,
          'location' : newlocation
    }
    context = {'user_info' : data}
    print(context)
    html = render(request, 'polls/profile.html', context)
    return HttpResponse(html)
    #return render(request, 'polls/profile.html', context)
