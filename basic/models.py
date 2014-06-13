from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    jabber = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()
    photo = models.ImageField(upload_to='uploads')

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)

        
class Location(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name