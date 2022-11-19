from django.test import TestCase
from .models import User

# Create your tests here.
class LoginTesting(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(id='1', username='jdelon02', email='chefjeremy@delongaz.com')
        
    def test_user_model(self):
        d = self.user
        self.assertTrue(isinstance(d, User))
        self.assertEqual(str(d.id), '1')
    
    
    