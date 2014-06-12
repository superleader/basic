from annoying.decorators import render_to
from basic.models import Person, Location


@render_to('index.html')
def index(request):
	person = Person.objects.get(pk=1)
	return locals()

	
@render_to('requests.html')
def requests(request):
	locations = Location.objects.all()[:10]
	return locals()