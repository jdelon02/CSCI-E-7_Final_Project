# FILE: steps/pageobjects/scrape.py
from behave_django.pageobject import PageObject, Link, Element


class Scrape(PageObject):

    page = 'scrape'  # view name, model or URL path

    elements = {
        'url': Element('form-control[name="url"]'),
        'submit': Link('css="btn-primary[type=submit"')
    }

    def select_url(self):
        self.url.set_text('https://www.foodnetwork.com/recipes/tyler-florence/cranberry-orange-sauce-recipe3-1946636')

    def click_scrape(self):
        self.submit.click()
