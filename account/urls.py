from django.conf.urls import url
from .views import AccountView, ChangePassword, MyTickets

urlpatterns = [
    url(r'^$', AccountView.as_view(), name='personal_account'),
    url(r'^change/', ChangePassword.as_view(), name='change_password'),
    url(r'^my_tickets/$', MyTickets.as_view(), name='my_tickets')
]
