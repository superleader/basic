from django import forms
from django.conf import settings 


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('%scss/jquery-ui-1.10.4.min.css' % settings.STATIC_URL,)
        }
        js = (
            '%sjs//jquery-ui-1.10.4.min.js' % settings.STATIC_URL,
            '%sjs/ui.datepicker.init.js' % settings.STATIC_URL
        )

    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(
            attrs={'class': 'vDateField', 'size': '10'})