from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tenant(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"tenant {self.profile.user.username}"


class Host(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"owner {self.profile.user.username}"


class Flat(models.Model):
    address = models.CharField(max_length=1000)
    surface = models.FloatField(blank=True, null=True)
    guests_number = models.IntegerField(default=1)
    rooms_number = models.IntegerField(default=2)
    hosts = models.ManyToManyField(Host)

    def __str__(self):
        return self.address


class Room(models.Model):

    ROOM_TYPES = (
        ('bedroom', 'bedroom'),
        ('kitchen', 'kitchen'),
        ('bathroom', 'bathroom'),
    )

    beds_number = models.IntegerField(default=1)
    room_type = models.CharField(default="bedroom", choices=ROOM_TYPES, max_length=8)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    devices_number = models.IntegerField(blank=True, null=True)


class Device(models.Model):
    entity_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    state = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)


class Rent(models.Model):
    hosts = models.ForeignKey(Host, on_delete=models.CASCADE)
    tenants = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, blank=True, null=True)
    begin_date = models.DateField()
    end_date = models.DateField()


class Sensors(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


class CheckOutTask(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    preferred_state = models.BooleanField(default=False)
