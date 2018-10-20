from django.contrib import admin

from .models import Profile, Host, Tenant

admin.site.register(Profile)
admin.site.register(Host)
admin.site.register(Tenant)