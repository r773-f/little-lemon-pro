from django.shortcuts import render
from .models import  Booking, Menu
from .serializers import BookingSerializer, MenuSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.core import serializers
from .forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json


def index(request):
    return render(request, 'index.html')

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def book(request):
    form = BookingForm
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(booking_date=data['booking_date']).filter(
            number_of_guest=data['number_of_guest']).exists()
        if exist==False:
            booking = Booking(
                name=data['name'],
                booking_date=data['booking_date'],
                number_of_guest=data['number_of_guest'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(booking_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    print("date: ", date)
    bookings = Booking.objects.all().filter(booking_date = date)
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {'bookings': booking_json})

def menu(request):
    menu_items = Menu.objects.all()
    return render(request, 'menu.html', {"menu": menu_items})

class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer