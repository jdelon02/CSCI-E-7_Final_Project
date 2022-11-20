from django.test import TestCase
from apps.recipes.models import Recipes
from apps.recipes.forms import recipesform
from apps.login.models import User

# Create your tests here.
import mock


class RecipeTesting(TestCase):

    def setUp(self):
        self.recipe = Recipes.objects.create(
            cookHour=1,
            cookMin=15,
            name='jdelon02 test recipe',
            description='JD Test Recipe',
            servingQuantity=3,
            prepHour=2,
            prepMin=30,
            skillLevel=3
        )

    def test_recipe_model(self):
        self.assertTrue(isinstance(self.recipe, Recipes))

    def test_recipe_cooktime(self):
        self.assertEqual(str(self.recipe.cookHour), '1')

    def test_recipe_cookMin(self):
        self.assertEqual(str(self.recipe.cookMin), '15')

    def test_recipe_name(self):
        self.assertEqual(str(self.recipe.name), 'jdelon02 test recipe')

    def test_recipe_description(self):
        self.assertEqual(str(self.recipe.description), 'JD Test Recipe')

    def test_recipe_servingQuantity(self):
        self.assertEqual(str(self.recipe.servingQuantity), '3')

    def test_recipe_prepHour(self):
        self.assertEqual(str(self.recipe.prepHour), '2')

    def test_recipe_prepMin(self):
        self.assertEqual(str(self.recipe.prepMin), '30')

    def test_recipe_skillLevel(self):
        self.assertEqual(str(self.recipe.skillLevel), '3')

    def test_recipe_save(self):

        testuser = mock.Mock(spec=User)
        testuser.username = 'testy'
        testuser.email = 'testy@mctesterston.com'
        testuser.password = 'Pass123'
        testrecipe = mock.Mock(spec=Recipes)
        testrecipe.name = self.recipe.name
        self.assertEqual(str(testrecipe.name), str(self.recipe.name))
        testrecipe.author = testuser
        testrecipe.cookHour = self.recipe.cookHour
        self.assertEqual(str(testrecipe.cookHour), str(self.recipe.cookHour))
        testrecipe.cookMin = self.recipe.cookMin
        self.assertEqual(str(testrecipe.cookMin), str(self.recipe.cookMin))
        testrecipe.description = self.recipe.description
        self.assertEqual(str(testrecipe.description), str(self.recipe.description))
        testrecipe.servingQuantity = self.recipe.servingQuantity
        self.assertEqual(str(testrecipe.servingQuantity), str(self.recipe.servingQuantity))
        testrecipe.prepHour = self.recipe.prepHour
        self.assertEqual(str(testrecipe.prepHour), str(self.recipe.prepHour))
        testrecipe.prepMin = self.recipe.prepMin
        self.assertEqual(str(testrecipe.prepMin), str(self.recipe.prepMin))
        testrecipe.skillLevel = self.recipe.skillLevel
        self.assertEqual(str(testrecipe.skillLevel), str(self.recipe.skillLevel))

    class Meta:
        app_label = 'recipes'
