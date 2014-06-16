from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_models
from sys import stderr


class Command(BaseCommand):
    def handle(self, *args, **options):
    	models = "error: Project models:\n%s" % \
        "\n".join(["%s - %s" % (m._meta.object_name, m.objects.count())
                   for m in get_models()])
        
        print >> stderr, models
        return models
        
