from django.shortcuts import render
# from django.http import HttpResponse
from .models import Post, Ride


def home(request):
    context={
        'my_ride': Ride.objects.filter(owner=request.user.username)
        # 'join_ride' : Ride.object.filter()
    }
    return render(request,'mysite/home.html',context)