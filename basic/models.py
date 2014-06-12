from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date = models.DateField()
    bio = models.TextField()
    contacts = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)

        
class Location(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name