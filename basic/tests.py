from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from basic.models import Person, Location


class BasicTest(TestCase):
	fixtures = ['initial_data.json']
	password = 'password'
	username = 'name'
    	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(self.username, 'tt@tt.com', \
		                                     self.password)
		#self.user.is_staff = True
		#self.user.save()
    
	def login(self):
		login = self.client.login(username=self.username, \
		                          password=self.password)
		self.failUnless(login, 'Could not log in')
        
	def test_index(self):
		response = self.client.get(reverse('home'))
		
		p = Person.objects.get(pk=1)
		self.failUnlessEqual(response.status_code, 200)
		self.assertContains(response, p.name)
		self.assertContains(response, p.surname)
		self.assertContains(response, p.date)
		self.assertContains(response, p.bio)
		self.assertContains(response, p.skype)
		self.assertContains(response, p.email)
		self.assertContains(response, p.jabber)
		self.assertContains(response, p.photo.url)
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
			
	def test_context_proccessor(self):
		response = self.client.get(reverse('home'))		
		self.failUnlessEqual(response.status_code, 200)
		self.assertContains(response, settings.LANGUAGE_CODE)

	def test_edit(self):
		data = {
		    'name': 'test_name',
		    'surname': 'test_surname',
		    'bio': 'test_bio',
		    'skype': 'test_skype',
		    'email': 'test_email@tt.tt',
		    'jabber': 'test_jabber',
		    'contacts': 'test_contacts',
		    'date': '2010-10-10',
		}
		
		response = self.client.get(reverse('edit-profile'))
		self.failUnlessEqual(response.status_code, 302)
		
		response = self.client.post(reverse('edit-profile'), data)
		# redirect to login-page
		self.failUnlessEqual(response.status_code, 302)
		
		self.login()
		response = self.client.get(reverse('edit-profile'))
		self.failUnlessEqual(response.status_code, 200)

		response = self.client.post(reverse('edit-profile'), data)
		# redirect to home-page
		self.failUnlessEqual(response.status_code, 302)
		p = Person.objects.get(pk=1)
		self.failUnlessEqual(data['name'], p.name)
		self.failUnlessEqual(data['surname'], p.surname)
		self.failUnlessEqual(data['bio'], p.bio)
		self.failUnlessEqual(data['skype'], p.skype)
		self.failUnlessEqual(data['email'], p.email)
		self.failUnlessEqual(data['jabber'], p.jabber)
		self.failUnlessEqual(data['date'], str(p.date))
		self.failUnlessEqual(data['contacts'], p.contacts)


		
		