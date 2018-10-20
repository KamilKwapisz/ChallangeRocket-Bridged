from django.contrib import admin

from .models import Profile, Host, Tenant, Device, Flat

admin.site.register(Profile)
admin.site.register(Host)
admin.site.register(Tenant)
admin.site.register(Device)
admin.site.register(Flat)
