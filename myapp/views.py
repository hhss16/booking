# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Booking
from django.http import JsonResponse
from django.core import serializers
from .forms import BookingForm
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# def home(request):
#     form = BookingForm()

#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         # print("FORM: ", form)
#         if form.is_valid():
#             # print("THIS: ", form)
#             form.save()

#     context = {"form" : form}
#     # print("HERE: ", context)
#     return render(request, 'booking.html', {"context" : context})


def home(request):
    form = BookingForm()
    today = datetime.today()
    bookings = Booking.objects.all().filter(reservation_date=today)
    context = {"form": form, "bookings": bookings,"today":today}
    return render(request, 'booking.html', context)


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')
