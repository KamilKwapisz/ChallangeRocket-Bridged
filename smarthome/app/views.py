from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.shortcuts import render
import homeassistant.remote as remote

from .forms import UserForm


def index(request):
    return render(request, "app/index.html", {})


def ajax(request):
    data = request.GET.dict()
    return JsonResponse(True, safe=False)


def logout_view(request):
    logout(request)
    context = {}
    return render(request, 'registration/logged_out.html', context)


def login(request, *args, **kwargs):
    return auth_views.login(request, *args, **kwargs)


class RegisterView(View):
    form_class = UserForm
    template_name = "registration/registration.html"

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.email = username
            user.set_password(password)
            user.save()

            # returns user object if credentials are OK
            user = authenticate(username=username, password=password)
            print(user)

            if user is not None:
                messages.success(self.request, "User {} has been created!".format(username))
            else:
                messages.error(self.request, "Invalid email or password")

        elif form.data['password'] != form.data['password_confirm']:
            form.add_error('password_confirm', 'Passwords do not match')

        return render(request, self.template_name, {'form': form})


def raspberry_connection():


    api = remote.API('http://172.16.230.225', 'tokyocommit')
    remote.get_state(api, 'binary_sensor.pir_office')
    state = remote.get_state(api, 'binary_sensor.pir_office').state  # on / off