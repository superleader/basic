from django.forms import ModelForm, DateField, Form, ChoiceField, RadioSelect

from basic.widgets import CalendarWidget
from basic.models import Person


class PersonForm(ModelForm):
	date = DateField(widget=CalendarWidget)
	
	class Meta:
	    model = Person
	    
	    
class PriorityForm(Form):
	priority = ChoiceField(required=False, widget=RadioSelect,
			choices=(('0', '0',), ('1', '1',)), initial=0)