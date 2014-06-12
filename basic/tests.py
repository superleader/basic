from django.test import Client, TestCase
from django.core.urlresolvers import reverse

from basic.models import Person, Location


class BasicTest(TestCase):
	fixtures = ['initial_data.json']
	
	def setUp(self):
		self.client = Client()
	
	def test_index(self):
		response = self.client.get(reverse('home'))
		
		p = Person.objects.get(pk=1)
		self.failUnlessEqual(response.status_code, 200)
		self.assertContains(response, p.name)
		self.assertContains(response, p.surname)
		self.assertContains(response, p.date)
		self.assertContains(response, p.bio)
		self.assertContains(response, p.contacts)
		
	def test_middleware(self):
		count = Location.objects.count()
		response = self.client.get(reverse('home'))
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(count + 1, Location.objects.count())
    
	def test_requests(self):
		response = self.client.get(reverse('first-requests'))
		self.failUnlessEqual(response.status_code, 200)
		for i in Location.objects.all()[:10]:
			self.assertContains(response, i)

        