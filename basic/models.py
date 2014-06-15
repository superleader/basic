from django.db import models
from django.db.models.loading import get_models
from django.db.models.signals import post_save, pre_delete
from django.db.models.signals import post_save, pre_delete


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

        
class Log(models.Model):
    object = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ACTION_CHOICES = (
        ('c', 'create'),
        ('u', 'update'),
        ('d', 'delete'),
    )
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    object_pk = models.PositiveIntegerField()


def save_object(sender, **kwargs):
    o = kwargs['instance']
    if kwargs['created']:
        a = 'create'
    else:
        a = 'update'

    log = Log(object_pk=o.pk, object=o._meta.object_name, action=a)
    log.save()


def delete_object(sender, **kwargs):
    o = kwargs['instance']
    log = Log(object_pk=o.pk, object=o._meta.object_name, action='delete')
    log.save()

for m in get_models():
    if m._meta.object_name not in ['Log', 'Session']:
        post_save.connect(save_object, m, dispatch_uid=m._meta.object_name)
        pre_delete.connect(delete_object, m, dispatch_uid=m._meta.object_name)