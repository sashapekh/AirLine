from django.conf.urls import include, url
from .views import PaymentVerify, VerifyPhone, SuccessPaymentPage


urlpatterns = [
    url(r'^(?P<ticket_id>[0-9]+)/(?P<price>[0-9]+)/$', PaymentVerify.as_view(), name='payment_main'),
    url(r'^verify/$', VerifyPhone.as_view(), name='verify_number'),
    url(r'^success/$', SuccessPaymentPage.as_view(), name='success_pay')
]
