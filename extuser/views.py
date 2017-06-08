from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, RedirectView
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

class Register(TemplateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print('method get')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            print('form saved')
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print('user logged')
            return redirect('index')
        else:
            print('user does not logged')
            return redirect('register')

        return render(request, self.template_name)


class Logout(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


