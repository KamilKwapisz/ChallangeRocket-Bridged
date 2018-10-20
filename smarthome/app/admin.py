from django.contrib import admin

from .models import Profile, Host, Tenant, Room, Rent

admin.site.register(Profile)
admin.site.register(Host)
admin.site.register(Tenant)
admin.site.register(Room)
admin.site.register(Rent)
