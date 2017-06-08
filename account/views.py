from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from account.forms import ChangePassword
from extuser.models import ExtUser
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib import messages
from ticketapp.models import OrderTicket
from django.core.mail import EmailMessage


# Create your views here.


class AccountView(TemplateView):
    template_name = 'account/account.html'


class ChangePassword(SuccessMessageMixin, FormView):
    template_name = 'account/change_password.html'
    form_class = ChangePassword
    success_url = '/'
    success_message = 'Пароль был изменен'

    def form_valid(self, form):
        user = ExtUser.objects.get(email=self.request.user)
        user.set_password(form.cleaned_data['confirm_password'])
        user.save()
        messages.add_message(self.request, messages.SUCCESS, '')
        return super(ChangePassword, self).form_valid(form)


class MyTickets(TemplateView):
    template_name = 'account/my_tickets.html'

    def get(self, request, *args, **kwargs):
        my_tickets = OrderTicket.objects.filter(user_fk_id=request.user.id).values(
            'code',
            'ticket_fk__pplan_ticket__plane_name',
            'ticket_fk__pplan_ticket__start_date',
            'ticket_fk__pplan_ticket__end_date',
            'ticket_fk__ticket_type__ticket_type',
            'ticket_fk__id'
        )
        print(kwargs)
        return render(request, self.template_name, {'my_tickets': my_tickets})

    def post(self, request):
        if len(request.POST['email']) != 0:
            ticket_info = OrderTicket.objects.filter(ticket_fk_id=request.POST['ticket_id']).values(
                'code',
                'ticket_fk__pplan_ticket__plane_name',
                'ticket_fk__pplan_ticket__start_date',
                'ticket_fk__pplan_ticket__end_date',
                'ticket_fk__ticket_type__ticket_type',
                'ticket_fk__place_number',
                'ticket_fk__pplan_ticket__terminal_fk_id__name'
            )
            email_message = "Номер билета > {0} \n" \
                            "Маршрут > {1} \n" \
                            "Дата вылета > {2} \n" \
                            "Дата прилёта > {3} \n" \
                            "Тип билета > {4} \n" \
                            "Место на рейсе > {5} \n" \
                            "Названия терминала отправки > {6}\n".format(
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
                                to=[request.POST['email']])
            mail.send()
            return redirect('my_tickets')
