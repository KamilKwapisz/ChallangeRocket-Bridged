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
    host = models.ForeignKey(Host, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.address


class Room(models.Model):

    ROOM_TYPES = (
        ('bedroom', 'bedroom'),
        ('kitchen', 'kitchen'),
        ('bathroom', 'bathroom'),
        ('other', 'other'),
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    beds_number = models.IntegerField(default=1,)
    room_type = models.CharField(choices=ROOM_TYPES, max_length=8, default="other")
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

    @property
    def devices(self):
        return Device.objects.filter(room=self.pk, is_allowed=True)

    @property
    def devices_number(self):
        return Device.objects.filter(room=self.pk, is_allowed=True).count()

    def save(self, *args, **kwargs):
        if not self.id and not self.name:
            self.name = self.room_type
        return super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} in flat {self.flat.address}"


class Device(models.Model):
    entity_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    is_allowed = models.BooleanField(default=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.entity_id})"


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
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    preferred_state = models.BooleanField(default=False)
