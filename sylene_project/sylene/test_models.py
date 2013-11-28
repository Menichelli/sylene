from django.test import TestCase
from sylene.models import all

class DocumentTestCase(TestCase):
	def setUp(self):
		hubertUser = User.objects.create(name = hubert)
		hubertUser.save()