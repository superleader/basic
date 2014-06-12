from annoying.decorators import render_to
from basic.models import Person


@render_to('index.html')
def index(request):
	person = Person.objects.get(pk=1)
	return locals()