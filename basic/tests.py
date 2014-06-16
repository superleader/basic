from django.test import Client, TestCase
from django.core.management import call_command
from django.template import Context, Template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.loading import get_models
from datetime import date
import sys
import os

from basic.models import Person, Location, Log


class BasicTest(TestCase):
	fixtures = ['initial_data.json']
	password = 'password'
	username = 'name'
    	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(self.username, 'tt@tt.com', \
		                                     self.password)
    
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
		for i in Location.objects.filter(priority=0)[:10]:
			self.assertContains(response, i)
		
		response = self.client.get(reverse('first-requests') + '?priority=1')
		self.failUnlessEqual(response.status_code, 200)
		for i in Location.objects.filter(priority=1)[:10]:
			self.assertContains(response, i)
		
		response = self.client.get(reverse('first-requests') + '?priority=0')
		self.failUnlessEqual(response.status_code, 200)
		for i in Location.objects.filter(priority=0)[:10]:
			self.assertContains(response, i)
			
	def test_context_proccessor(self):
		response = self.client.get(reverse('home'))		
		self.failUnlessEqual(response.status_code, 200)
		self.assertContains(response, settings.LANGUAGE_CODE)

	def test_edit(self):		
		# redirect to login-page
		response = self.client.get(reverse('edit-profile'))
		self.failUnlessEqual(response.status_code, 302)
		
		self.login()
		response = self.client.get(reverse('edit-profile'))
		self.failUnlessEqual(response.status_code, 200)
	
	def test_save(self):
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
	
		response = self.client.post(reverse('save-profile'), data)
		#redirect to login page
		self.failUnlessEqual(response.status_code, 302)
		
		self.login()
		response = self.client.get(reverse('save-profile'), data)
		# doeant supprt GET method
		self.failUnlessEqual(response.status_code, 405)
		
		response = self.client.post(reverse('save-profile'), data)
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.content, '{"result": 1}')
		p = Person.objects.get(pk=1)
		self.failUnlessEqual(data['name'], p.name)
		self.failUnlessEqual(data['surname'], p.surname)
		self.failUnlessEqual(data['bio'], p.bio)
		self.failUnlessEqual(data['skype'], p.skype)
		self.failUnlessEqual(data['email'], p.email)
		self.failUnlessEqual(data['jabber'], p.jabber)
		self.failUnlessEqual(data['date'], str(p.date))
		self.failUnlessEqual(data['contacts'], p.contacts)	
		
	def test_tag_edit_link(self):
		response = Template("{% load basic_urls %}{% edit_link user %}").render(
		    Context({"user": self.user}))
		c = self.user.__class__
		self.failUnlessEqual(response, reverse('admin:%s_%s_change' %  \
		    (c._meta.app_label, c._meta.module_name), args=[self.user.pk]))
	
	def test_print_models(self):
		sys.stdout = open('dump_mycommand.txt', 'w')
		call_command('print_models')
		sys.stdout.close()
		sys.stdout = sys.__stdout__
		
		f = file('dump_mycommand.txt', "r")
		result = "Project models:\n%s" % \
		    "\n".join(["%s - %s" % (m._meta.object_name, m.objects.count())
		                 for m in get_models()])
		self.failUnlessEqual(f.read().strip('\n'), result.strip('\n'))
		f.close()
		os.remove('dump_mycommand.txt')
		
	def test_bash_script(self):
		os.system('./print_models')
		file = './%s.dat' % date.today().strftime("%Y-%m-%d")
		self.failUnlessEqual(
			os.path.exists('./%s.dat' % date.today().strftime("%Y-%m-%d")), True)
		os.remove(file)
		
	def test_signals(self):
		count = Log.objects.count()
		
		l = Location(name='/')
		l.save()
		log_count = Log.objects.count()
		self.failUnlessEqual(Log.objects.all()[log_count - 1].action, 'create')
		self.failUnlessEqual(count + 1, log_count)
		
		l.name = ""
		l.save()
		log_count = Log.objects.count()
		self.failUnlessEqual(Log.objects.all()[log_count - 1].action, 'update')
		self.failUnlessEqual(count + 2, log_count)
		
		l.delete()
		log_count = Log.objects.count()
		self.failUnlessEqual(count + 3, log_count)
		self.failUnlessEqual(Log.objects.all()[log_count - 1].action, 'delete')
