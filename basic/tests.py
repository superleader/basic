from django.test import Client, TestCase
from basic.models import Person


class BasicTest(TestCase):
	fixtures = ['initial_data.json']
	
	def test_index(self):
		response = Client().get('/')
		
		p = Person.objects.get(pk=1)
		self.assertContains(response, p.name)
		self.assertContains(response, p.surname)
		self.assertContains(response, p.date)
		self.assertContains(response, p.bio)
		self.assertContains(response, p.contacts)