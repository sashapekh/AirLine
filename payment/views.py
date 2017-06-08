from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketapp.models import Ticket, OrderTicket
from twilio.rest import Client
import random
from django.core.mail import EmailMessage

# custom views display


class PaymentVerify(LoginRequiredMixin, TemplateView):
    template_name = 'payment/payment.html'
    login_url = '/register/'

    def get(self, request, ticket_id, price, *args, **kwargs):
        ticket = Ticket.objects.filter(id=ticket_id).values(
            'id',
            'pplan_ticket__plane_name',
            'pplan_ticket__start_city_name__name',
            'pplan_ticket__end_city_name__name',
            'ticket_type__price',
            'ticket_type__ticket__place_number',
            'pplan_ticket__ticket__ticket_type'
        )
        request.session['ticket'] = ticket[0]
        request.session['price'] = price
        request.session['ticket_id'] = ticket_id
        print(type(str(request.user)))
        return render(request, self.template_name, {'price': price})

    def post(self, request, *args, **kwargs):
        # send code to customer phone
        code = random.randint(1, 1000000)
        request.session['code'] = code
        client = Client('AC410132c8bd44ed00f7f4539559884283', '47bd5593b50b4a7a46aa164542238016')
        client.messages.create(to=request.POST['verify_phone_number'],
                               from_='+18582958048',
                               body=' your verify code = {}'.format(str(request.session['code']))
                               )
        return redirect('verify_number')


class VerifyPhone(TemplateView):
    template_name = 'payment/verify_code_phone.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        if request.session['code'] == int(request.POST['verify_code']):
            return redirect('success_pay')
        else:
            return render(request, self.template_name)


class SuccessPaymentPage(TemplateView):
    template_name = 'payment/success_pay.html'

    def get(self, request, *args, **kwargs):
        ticket = OrderTicket(ticket_fk_id=request.session['ticket_id'],
                             user_fk_id=request.user.id,
                             code=random.randint(1, 1000000),
                             status='куплен')
        ticket.save()
        ticket_info = OrderTicket.objects.filter(ticket_fk_id=request.session['ticket_id']).values(
            'code',
            'ticket_fk__pplan_ticket__plane_name',
            'ticket_fk__pplan_ticket__start_date',
            'ticket_fk__pplan_ticket__end_date',
            'ticket_fk__ticket_type__ticket_type',
            'ticket_fk__place_number',
            'ticket_fk__pplan_ticket__terminal_fk_id__name'
        )
        email_message = "Номер купленого вами билета -------- {0} \n" \
                        "Маршрут -------- {1} \n" \
                        "Дата вылета -------- {2} \n" \
                        "Дата прилёта -------- {3} \n" \
                        "Тип билета -------- {4} \n" \
                        "Место на рейсе -------- {5} \n" \
                        "Названия терминала отправки -------- {6}\n".format(
            ticket_info[0]['code'],
            ticket_info[0]['ticket_fk__pplan_ticket__plane_name'],
            ticket_info[0]['ticket_fk__pplan_ticket__start_date'],
            ticket_info[0]['ticket_fk__pplan_ticket__end_date'],
            ticket_info[0]['ticket_fk__ticket_type__ticket_type'],
            ticket_info[0]['ticket_fk__place_number'],
            ticket_info[0]['ticket_fk__pplan_ticket__terminal_fk_id__name']
        )

        mail = EmailMessage('ticket №{}'.format(ticket_info[0]['code']),
                            email_message,
                            to=[str(request.user)])
        mail.send()
        return render(request, self.template_name)
