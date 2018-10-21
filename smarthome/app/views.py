from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.shortcuts import render

from random import randint

from .forms import UserForm
from .models import Room, Host, Profile, Flat, Device, Tenant, Rent, CheckOutTask

import homeassistant.remote as remote


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


def flats_list(request):
    username = request.user.username
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    host = Host.objects.get(profile=profile)
    user_flats = Flat.objects.filter(host=host)
    context = dict(flats=user_flats)

    return render(request, "app/flats_list.html", context)


class FlatDetailView(DetailView):
    model = Flat
    template_name = "app/flat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flat = self.get_object()
        context['flat'] = flat
        rooms = Room.objects.filter(flat=flat)
        context['rooms'] = rooms

        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "app/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        devices = Device.objects.filter(room=room, is_allowed=True)
        context['room'] = room
        context['devices'] = devices
        tasks = list()
        for device in devices:
            tasks += list(CheckOutTask.objects.filter(device=device))
        context['tasks'] = tasks

        return context


def host_device_permission(request, room_pk):
    room = Room.objects.get(pk=room_pk)
    devices = Device.objects.filter(room=room)
    context = dict(devices=devices)
    context['room'] = room

    return render(request, "app/room_permissions.html", context)


def ajax_change_device_permission(request):
    data = request.GET.dict()
    device_id = data['device_id']
    is_allowed = data['is_allowed']
    device = Device.objects.get(pk=device_id)
    device.is_allowed = is_allowed
    device.save()
    return JsonResponse(True, safe=False)


def ajax_add_checkout_task(request):
    data = request.GET.dict()
    device_id = data['device_id']
    device = Device.objects.get(pk=device_id)
    task = data['task']
    state = data['preferred_state']
    if CheckOutTask.objects.filter(device=device).count() > 1:
        check_task = CheckOutTask.objects.get(device=device)
        check_task.preferred_state = state
        check_task.task = task
    else:
        CheckOutTask.objects.create(device=device, task=task, preferred_state=state)
    return JsonResponse(True, safe=False)


def ajax_validate_access_code(request):
    data = request.GET.dict()
    flat_id = int(data['flat_id'])
    code = data['code']
    valid_code = Flat.objects.get(pk=flat_id).access_code
    if valid_code == code and len(code) == 4:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


def access_code(request, flat_pk):
    context = dict(flat_id=flat_pk)
    return render(request, "app/keypad.html", context)


def change_device_state(request, device_id, state):
    if device_id:
        device = Device.objects.get(entity_id=device_id)
        if state == "on":
            device.state = True
        elif state == "off":
            device.state = False
        device.save()
    return HttpResponse("hello")


def change_access_code(request, flat_pk):
    flat = Flat.objects.get(pk=flat_pk)
    code = ""
    for i in range(4):
        val = randint(1, 9)
        code += str(val)
    flat.access_code = code
    flat.save()
    return HttpResponse("changed")


