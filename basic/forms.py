from django.forms import ModelForm, DateField

from basic.widgets import CalendarWidget
from basic.models import Person


class PersonForm(ModelForm):
	date = DateField(widget=CalendarWidget)
	
	class Meta:
	    model = Person