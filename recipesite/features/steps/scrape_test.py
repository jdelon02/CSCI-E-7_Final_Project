# features/steps/scrape_test.py
import requests
from behave import *
from steps.pageobjects.scrape import Scrape
from recipe_scrapers import scrape_me, scrape_html

URL = 'https://www.foodnetwork.com/recipes/tyler-florence/cranberry-orange-sauce-recipe3-1946636'
TEXT = 'Cranberry-Orange Sauce'


@given('I visit the scrape page')
def send_request_page(context):
    context.scrape_page = Scrape(context)
    assert context.scrape_page.response.status_code == 200


@then('I scrape a recipe')
def get_recipe_page(context):
    context.response = requests.get(URL)
    assert context.response.status_code == 200


@then('I expect the response to be parsed as recipe')
def check_response_title_contains(context):
    # context.response = requests.get(URL).text
    recipe_scrapes = scrape_html(html=context.response.text, org_url=URL)
    assert TEXT in recipe_scrapes.title()


@then('I expect the ingrdeients to not be empty')
def check_response_ingred_notempty(context):
    # context.response = requests.get(URL).text
    recipe_scrapes = scrape_html(html=context.response.text, org_url=URL)
    assert recipe_scrapes.ingredients() != ''
