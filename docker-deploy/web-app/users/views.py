from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from mysite.models import Ride, Sharer
from .forms import UserRegisterForm, RideForm, SearchRideForm, PartyConfirmForm
from django.contrib.auth.decorators import login_required
from driver.forms import driveruser, update_profile_form
from .models import Profile



def register(request):
    # 创建一个新的user
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'account creat successful, you are able to login')
            # 返回首页
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})



# user must log in to view the profile page
@login_required
def profile(request):
    username = request.user.username
    instance = Profile.objects.get(username=username)
    context = {'u_form': instance}
    return render(request, 'users/profile.html', context)


def update_profile(request):
    if request.method=='POST':
        # username = request.user.username
        # instance = Profile.objects.get(username=username)
        # context = { 'u_form': instance }
        u_form = update_profile_form (request.POST)
        if u_form.is_valid():
            data = u_form.cleaned_data
            p = Profile.objects.get(username=request.user.username)
            p.vehicle_type_registered = data['vehicle_type_registered']
            p.license_plate_number = data['license_plate_number']
            p.capacity_of_the_car = data['capacity_of_the_car']
            p.spacial_request = data['spacial_request']
            p.save()
        return render(request, 'users/profile.html', {'u_form': Profile.objects.get(username=request.user.username)})
    else:
        form = update_profile_form()
    return render(request, 'users/update_profile.html',{'form':form})


@login_required
def driver(request):
    username = request.user.username
    try:
        instance = Profile.objects.get(username=username)
        context = {'rides': Ride.objects.filter(driver=username), 'profile': instance}
        return render(request, 'users/driver.html', context)
    except:
        form = driveruser()
        return render(request, 'users/driver_register.html', {'form': form})
    # user_id = request.user.id
    # instance = get_object_or_404(Profile, user_id=user_id)
    # return render(request,'users/driver.html', {'form': instance})



def request_ride(request):
    if request.method == 'POST':
        ride_form = RideForm(request.POST)
        if ride_form.is_valid():
            instance = ride_form.save(commit=False)
            instance.owner = request.user.username
            instance.status = 0
            instance.save()
            return HttpResponseRedirect('/details/%d' % instance.id)
    ride_form = RideForm()
    return render(request, 'users/request_ride.html', {'form': ride_form})


def edit_ride(request, ride_id):
    if request.method == 'POST':
        ride_form = RideForm(request.POST)
        if ride_form.is_valid():
            instance = ride_form.save(commit=False)
            instance.id = ride_id
            instance.owner = request.user.username
            instance.status = 0
            instance.save()
            return HttpResponseRedirect('/details/%d' % instance.id)
            # return render(request ,'details/%d' % instance.id)
    instance = get_object_or_404(Ride, id=ride_id)
    ride_form = RideForm(instance=instance)
    return render(request, '/edit_ride/%d' % ride_id, {'form': ride_form})

def ride_details(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    # render the page
    return render(request, 'users/detail.html', {'ride': ride})


def search_ride(request):
    if request.method == 'POST':
        form = SearchRideForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rides = Ride.objects.filter(arrival_time__range=(data['earliest_arrival_time'], data['latest_arrival_time']),
                                        destination=data['destination'], to_join=True, status=0)
            return render(request, 'users/search_result.html', {'rides': rides})
    form = SearchRideForm()
    return render(request, 'users/search_ride.html', {'form': form})

def join_ride(request, ride_id):
    if request.method == 'POST':
        form = PartyConfirmForm(request.POST)
        if form.is_valid():
            party = form.cleaned_data['party']
            info = Sharer.objects.create(ride_id=ride_id, sharer=request.user.username, party=party)
            info.save()
            messages.success(request, f'Join successful')
            join_rides = []
            for r in Sharer.objects.filter(sharer=request.user.username):
                qs = Ride.objects.filter(id=r.ride_id, status__lt=2)
                if qs:
                    join_rides.append(qs[0])
            context = {'my_ride': Ride.objects.filter(owner=request.user.username), 'join_ride': join_rides}
            return render(request, 'mysite/home.html', context)
    form = PartyConfirmForm()
    return render(request, 'join_ride.html', {'form': form})


def complete_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 2
    ride.save()
    return render(request, 'mysite/home.html')


def cancel_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 3
    ride.save()
    return render(request, 'mysite/home.html')

def confirm_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 1
    username = request.user.username
    ride.driver = username
    ride.save()
    return render(request, 'users/driver.html')

