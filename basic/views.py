from annoying.decorators import render_to, ajax_request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from basic.widgets import CalendarWidget
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
	form = PersonForm(instance=Person.objects.get(pk=1))	
	calendar = CalendarWidget()
	return locals()
	

@login_required
@require_POST
@ajax_request
def save(request):
	form = PersonForm(request.POST, request.FILES, instance=Person.objects.get(pk=1))
	if form.is_valid():
		form.save()
		return {'result': 1}
	else:
		return {'result': 0, 'errors': form.errors}
	
	