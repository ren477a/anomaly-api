from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import traceback
import json


User = get_user_model()


class Person(models.Model):
    ROLE_OWNER = 'OWNER'
    ROLE_PERSONNEL = 'PERSONNEL'
    ROLE_CHOICES = (
        (ROLE_OWNER, 'Owner'),
        (ROLE_PERSONNEL, 'Personnel'),
    )

    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.CharField(max_length=250)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    admin = models.ForeignKey('self', related_name='underlings', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Camera(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    owner = models.ForeignKey(Person, related_name='cameras', on_delete=models.CASCADE, null=True)

    def __str__(self):
      return self.name


class Notification(models.Model):
    TYPE_ABUSE = 'ABUSE'
    TYPE_ARREST = 'ARREST'
    TYPE_ARSON = 'ARSON'
    TYPE_ASSAULT = 'ASSAULT'
    TYPE_BURGLARY = 'BURGLARY'
    TYPE_EXPLOSION = 'EXPLOSION'
    TYPE_FIGHTING = 'FIGHTING'
    TYPE_ACCIDENTS = 'ACCIDENTS'
    TYPE_ROBBERY = 'ROBBERY'
    TYPE_SHOOTING = 'SHOOTING'
    TYPE_SHOPLIFTING = 'SHOPLIFTING'
    TYPE_STEALING = 'STEALING'
    TYPE_VANDALISM = 'VANDALISM'
    TYPE_NORMAL = 'NORMAL'

    TYPE_CHOICES = (
        (TYPE_ABUSE, 'Abuse'),
        (TYPE_ARREST, 'Arrest'),
        (TYPE_ARSON, 'Arson'),
        (TYPE_ASSAULT, 'Assault'),
        (TYPE_BURGLARY, 'Burglary'),
        (TYPE_EXPLOSION, 'Explosion'),
        (TYPE_FIGHTING, 'Fighting'),
        (TYPE_ACCIDENTS, 'Road Accidents'),
        (TYPE_ROBBERY, 'Robbery'),
        (TYPE_SHOOTING, 'Shooting'),
        (TYPE_SHOPLIFTING, 'Shoplifting'),
        (TYPE_STEALING, 'Stealing'),
        (TYPE_VANDALISM, 'Vandalism'),
        (TYPE_NORMAL, 'Normal event'),
    )

    _type = models.CharField(max_length=250, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField()
    camera = models.ForeignKey(Camera, related_name='notifications', on_delete=models.CASCADE)

    def __str__(self):
      return "{} - {}".format(self._type, self.camera)


@receiver(post_save, sender=Notification)
def send_notif_after_save(sender, instance, **kwargs):
    print("Signal from post_save fired {}".format(instance.timestamp))
    channel_layer = get_channel_layer()
    try:
        user_id = instance.camera.owner.user.pk
    except:
        print("[Error] Unable to send notif err={}".format(traceback.format_exc()))
        return
    group_name = "user_{}".format(user_id)
    async_to_sync(channel_layer.group_send)(
    group_name,
    {
        "type": "chat.message",
        "message": {
            "type": instance._type,
            "timestamp": instance.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "camera": instance.camera.name
        },
    }
)