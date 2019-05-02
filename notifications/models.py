from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Person(models.Model):
    ROLE_OWNER = 'OWNER'
    ROLE_PERSONNEL = 'PERSONNEL'
    ROLE_CHOICES = (
        (ROLE_OWNER, 'Owner'),
        (ROLE_PERSONNEL, 'Personnel'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.CharField(max_length=250)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


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