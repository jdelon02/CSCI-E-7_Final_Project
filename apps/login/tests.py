from django.test import TestCase
from apps.login.models import User

# Create your tests here.


class LoginTesting(TestCase):

    def setUp(self):
        self.user = User.objects.create(id='1', username='jdelon02', email='chefjeremy@delongaz.com')

    def test_user_model(self):
        d = self.user
        self.assertTrue(isinstance(d, User))
        self.assertEqual(str(d.id), '1')
        self.assertEqual(str(d.email), 'chefjeremy@delongaz.com')
        self.assertEqual(str(d.username), 'jdelon02')

    class Meta:
        app_label = 'login'
