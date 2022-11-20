from django.test import TestCase
from apps.recipes.models import Recipes

# Create your tests here.


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

    class Meta:
        app_label = 'recipes'
