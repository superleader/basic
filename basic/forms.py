from django.forms import ModelForm

from basic.models import Person


class PersonForm(ModelForm):

    class Meta:
        model = Person