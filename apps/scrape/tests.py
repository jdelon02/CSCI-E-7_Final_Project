from django.test import TestCase
import cloudscraper
from recipe_scrapers import scrape_me, scrape_html
from apps.scrape.forms import ScrapeForm

# Create your tests here.


class ScrapeTesting(TestCase):

    def setUp(self):
        self.url = 'https://www.foodnetwork.com/recipes/tyler-florence/cranberry-orange-sauce-recipe3-1946636'
        self.scraper = cloudscraper.create_scraper()
        self.recipe_scrapes = self.scraper.get(self.url).text
        if self.recipe_scrapes:
            self.recipe = scrape_html(html=self.recipe_scrapes, org_url=self.url)
        self.attributes = dir(self.recipe)

    def test_scrape_title(self):
        self.assertIsNotNone(str(self.recipe.title()))
        # print(dir(self.recipe))

    def test_scrape_ingredients(self):
        self.assertIsNotNone(str(self.recipe.ingredients()))

    def test_scrape_instructions(self):
        self.assertIsNotNone(str(self.recipe.instructions()))

    def test_scrape_instruction_list(self):
        self.assertIsNotNone(str(self.recipe.instructions_list()))

    def test_scrape_total_time(self):
        self.assertIsNotNone(str(self.recipe.total_time()))

    def test_scrape_yields(self):
        self.assertIsNotNone(str(self.recipe.yields()))

    class Meta:
        app_label = 'scrape'
