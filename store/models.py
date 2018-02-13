from django.db import models


class Artist(models.Model):
    name = models.CharField('nom', max_length=200, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "artiste"


class Contact(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField('nom', max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "prospect"


class Album(models.Model):
    reference = models.IntegerField('référence', blank=True, null=True)
    created_at = models.DateTimeField('crée le', auto_now_add=True)
    available = models.BooleanField('disponible', default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField('image')
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "disque"


class Booking(models.Model):
    created_at = models.DateTimeField('crée le ', auto_now_add=True)
    contacted = models.BooleanField('contacté', default=False)
    album = models.OneToOneField(Album)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name
    class Meta:
        verbose_name = "réservation"
