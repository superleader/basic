from django import template
from django.core.urlresolvers import reverse
from django.contrib import admin
register = template.Library()


@register.simple_tag
def edit_link(o):
    return reverse('admin:%s_%s_change' % (o.__class__._meta.app_label, \
        o.__class__._meta.module_name), args=[o.pk])