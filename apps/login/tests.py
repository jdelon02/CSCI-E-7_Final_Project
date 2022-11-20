from django.test import TestCase
from apps.login.models import User

# Create your tests here.


class LoginTesting(TestCase):

    def setUp(self):
        self.user = User.objects.create(id='1', username='jdelon02', email='chefjeremy@delongaz.com')

    def test_user_model(self):
        self.assertTrue(isinstance(self.user, User))

    def test_user_id_model(self):
        self.assertEqual(str(self.user.id), '1')

    def test_user_email_model(self):
        self.assertEqual(str(self.user.email), 'chefjeremy@delongaz.com')

    def test_user_username_model(self):
        self.assertEqual(str(self.user.username), 'jdelon02')

    class Meta:
        app_label = 'login'
