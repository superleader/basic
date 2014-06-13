from annoying.decorators import render_to
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from basic.models import Person, Location
from basic.forms import PersonForm


@render_to('index.html')
def index(request):
	person = Person.objects.get(pk=1)
	return locals()

	
@render_to('requests.html')
def requests(request):
	locations = Location.objects.all()[:10]
	return locals()
	

@login_required
@render_to('edit.html')
def edit(request):
	if request.method == 'POST':
		form = PersonForm(request.POST, request.FILES, instance=Person.objects.get(pk=1))
		if form.is_valid():
			form.save()
			return redirect('home')
		else:
			print form.errors
	else:
		form = PersonForm(instance=Person.objects.get(pk=1))
		
	
	return locals()