from django.conf.urls import url
from .views import SearchTicket, TicketBooking, HotelsView, HotelOrder

urlpatterns = [
    url(r'^ticket/$', SearchTicket.as_view(), name='ticket_search'),
    url(r'^ticket_booking/(?P<ticket_id>[0-9]+)/(?P<planeplan_id>[0-9]+)/$',
        TicketBooking.as_view(),
        name='ticket_booking'),
    # display hotel to reservation
    url(r'^hotels/$', HotelsView.as_view(), name='hotels'),
    url(r'^hotel/(?P<hotel_id>[0-9]+)/$', HotelOrder.as_view(), name='hotel_order')

]
