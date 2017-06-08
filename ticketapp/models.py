from django.db import models
from extuser.models import ExtUser
from AirLine import settings
from AirLine.settings import BASE_DIR


# Create your models here.

class CityManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class City(models.Model):
    object = CityManager()
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, default='City', max_length=200)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)


class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(null=False, default='hotel name', max_length=200)
    city_hotel_fk = models.ForeignKey(City, on_delete=models.CASCADE)
    h_stars = models.IntegerField(null=False, default=1)
    street = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True)
    day_price = models.IntegerField(null=False, default=1000)

    def __str__(self):
        return "Hotel name - {0}, location {1}, stars {2}".format(self.hotel_name,
                                                                  Hotel.objects.filter(id=self.id).values(
                                                                      'city_hotel_fk__name')[0]['city_hotel_fk__name'],
                                                                  str(self.h_stars))


class TicketType(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(null=False, default='buisness/econom', max_length=100)
    price = models.FloatField(max_length=100)

    def __str__(self):
        return 'type - {0}, price {1}'.format(self.ticket_type, str(self.price))


# таблица имен терминалов аэропорта
class TerminalName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.name


class PlanePlan(models.Model):
    id = models.AutoField(primary_key=True)
    # дата вылета рейса
    start_date = models.DateField()
    # дата прилёта рейса
    end_date = models.DateField()
    # название самолёта
    plane_name = models.CharField(max_length=100, null=False, default='plane name')
    # название аеропорта от куда летит самолёт
    airport_name_start = models.CharField(max_length=100, null=False, default='airport name')
    # название аеропорта прибытия
    airport_name_end = models.CharField(max_length=100, null=False, default='airport name')
    terminal_fk = models.ForeignKey(TerminalName, on_delete=models.CASCADE)
    # название города от куда вылетает самолёт
    start_city_name = models.ForeignKey(City, on_delete=models.CASCADE, related_name='start_city_name')
    # название города куда прилетает самолёт
    end_city_name = models.ForeignKey(City, on_delete=models.CASCADE, related_name='end_city_name')

    def __str__(self):
        return ' start from {0} (date {1}), finish in {2} (destination time {3})'.format(self.start_city_name,
                                                                                         self.start_date,
                                                                                         self.end_city_name,
                                                                                         self.end_date)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    # номер места в самолёте
    place_number = models.IntegerField(null=False, default=1)
    # компания которая проводит перелёт
    company_name = models.CharField(null=True, max_length=100)
    pplan_ticket = models.ForeignKey(PlanePlan, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)

    def __str__(self):
        return 'plane number = {0}, company name = {1},' \
               'ticket plan = {2}, ticket type = {3}'.format(
            self.place_number,
            self.company_name,
            self.pplan_ticket,
            self.ticket_type
        )


# билет который непосредственно забронировал/купил пользователь
class OrderTicket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_fk = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(ExtUser, on_delete=models.CASCADE)
    wishes_text = models.TextField(null=True)
    code = models.IntegerField(null=False, default=1)
    status = models.CharField(max_length=50, null=False, default='бронь')

    def __str__(self):
        return 'ticket {0}, user {1}'.format(self.ticket_fk, self.user_fk)


# create hotel room info info
class HotelRoom(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_fk = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=3)
    room_type = models.CharField(max_length=100, null=False, default='Обычный')
    price = models.IntegerField(default=100, null=False)

    def __str__(self):
        return "room type = {0} | price = {1} | hotel name = {2}".format(self.room_type, str(self.price),
                                                                         HotelRoom.objects.filter(id=self.id).values(
                                                                             'hotel_fk__hotel_name'
                                                                         )[0]['hotel_fk__hotel_name'])


class ReservationRoomInfo(models.Model):
    id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=100, null=True)
    room_numbers = models.IntegerField(null=True)
    person_number = models.IntegerField(null=True)
    food_delivery = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return 'номер  {0}, количество персон {1}, заезд {2} выезд {3}'.format(
            self.room_type, str(self.person_number), self.start_date, self.end_date
        )


class OrderHotel(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_fk = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(ExtUser, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100, null=True)
    room_numbers = models.IntegerField(null=True)
    person_number = models.IntegerField(null=True)
    food_delivery = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_price = models.IntegerField(null=True)

    def __str__(self):
        return str(self.hotel_fk_id)
