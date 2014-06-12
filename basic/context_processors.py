from django.conf import settings


def mysettings(request):
    return {'settings': settings}