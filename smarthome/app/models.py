from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tenant(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Host(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Room(models.Model):
    address = models.CharField(max_length=1000)
    surface = models.FloatField(blank=True, null=True)
    guests_number = models.IntegerField(default=1)
    bedrooms_number = models.IntegerField(default=1)
    bathrooms_number = models.IntegerField(default=1)
    owners = models.ManyToManyField(Host)


class Rent(models.Model):
    hosts = models.ForeignKey(Host, on_delete=models.CASCADE)
    tenants = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField()


class Sensors(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
