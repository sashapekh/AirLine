from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.contrib.messages.views import SuccessMessageMixin

from django.core import serializers


# Create your views here.


class SearchTicket(LoginRequiredMixin, TemplateView):
    template_name = 'ticket_view/search_ticket.html'
    login_url = '/register/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        # email = EmailMessage('title', 'body', to=['ska8r@i.ua'])
        # email.send()
        return render(request, self.template_name, )

    def post(self, request):
        ticket_result = request.POST
        search_error = ''
        planeplan = PlanePlan.objects.filter(
            start_city_name__name=ticket_result['start_fly_name'],
            end_city_name__name=ticket_result['end_fly_name'],
            start_date=ticket_result['start_fly'],
            ticket__orderticket__code__isnull=True,
            ticket__ticket_type__ticket_type=ticket_result[
                'ticket_type']).values(
            'id',
            'start_city_name__name',
            'end_city_name__name',
            'airport_name_start',
            'airport_name_end',
            'start_date',
            'end_date',
            'ticket__ticket_type__price',
            'ticket__place_number',
            'ticket__ticket_type__ticket_type',
            'ticket__id'
        )
        print(int(planeplan[0]['ticket__ticket_type__price']))
        if planeplan.__len__() == 0:
            search_error = "Ничего не найдено, попробуйте снова :("

        return render(request, self.template_name, {'planeplan': planeplan,
                                                    'search_error': search_error})


class TicketBooking(SuccessMessageMixin, TemplateView):
    template_name = 'ticket_view/ticket_booking.html'
    success_url = '/account/'
    success_message = 'Билет успешно забронирован'

    def get(self, request, planeplan_id, ticket_id, *args, **kwargs):
        ticket_query = PlanePlan.objects.filter(id=planeplan_id, ticket__id=ticket_id).values(
            'start_city_name__name',
            'end_city_name__name',
            'airport_name_start',
            'airport_name_end',
            'start_date',
            'end_date',
            'ticket__ticket_type__price',
            'ticket__place_number',
            'ticket__ticket_type__ticket_type',
            'terminal_fk__name',
            'ticket__id'

        )
        return render(request, self.template_name, {'ticket_query': ticket_query})

    def post(self, request, planeplan_id, ticket_id, *args, **kwargs):
        if request.POST['confirm']:
            ticket = OrderTicket(ticket_fk_id=ticket_id,
                                 user_fk_id=request.user.id,
                                 code=random.randint(1, 1000000))
            ticket.save()
            return redirect('my_tickets', *args, **kwargs)


class HotelsView(TemplateView):
    template_name = 'hotel/hotels.html'

    def get(self, request, *args, **kwargs):
        hotels = Hotel.objects.all().values(
            'id',
            'city_hotel_fk__name',
            'hotel_name',
            'street',
            'description',
            'image',
            'h_stars'
        )

        return render(request, self.template_name, {'hotels': hotels})


class HotelOrder(TemplateView):
    template_name = 'hotel/order_hotel.html'

    def get(self, request, hotel_id, *args, **kwargs):
        hotel_info = Hotel.objects.filter(id=hotel_id).values(
            'hotel_name',
            'hotelroom__room_type',
            'hotelroom__price'

        )
        print(hotel_info)
        return render(request, self.template_name, {'hotel_name': hotel_info[0]['hotel_name'],
                                                    'hotel_info': hotel_info})

    def post(self, request, hotel_id, *args, **kwargs):
        if int(request.POST['person_number']) > 0 and int(request.POST['room_number']):
            room_price_type = str(request.POST['room_type']).split(',')
            end_price = int(request.POST['person_number']) * int(request.POST['room_number']) * int(room_price_type[0])
            order = OrderHotel(
                hotel_fk_id=hotel_id,
                user_fk_id=request.user.id,
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                food_delivery=request.POST['food_room'],
                room_type=room_price_type[1],
                room_numbers=int(request.POST['room_number']),
                person_number=int(request.POST['person_number']),
                total_price=end_price
            )
            order.save()
        return redirect('hotel_order', hotel_id=hotel_id)
