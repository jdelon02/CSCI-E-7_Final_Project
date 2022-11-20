# features/steps/scrape_test.py
import requests
from behave import *
from recipe_scrapers import scrape_me, scrape_html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://www.foodnetwork.com/recipes/tyler-florence/cranberry-orange-sauce-recipe3-1946636'
TEXT = 'Cranberry-Orange Sauce'
NEWURL = ''


@given('I log into the site')
def login_to_site(context):
    # Login to the Admin Panel
    context.selenium.get('http://127.0.0.1:8000/login/')
    # Fill Login Information
    username = context.selenium.find_element("name", "username")
    username.send_keys("admin")
    password = context.selenium.find_element("name", "password")
    password.send_keys("admin")
    submit = context.selenium.find_element("xpath", '//input[@value="Login"]')
    submit.click()
    # Locate login button and click on it
    # context.selenium.find_element_by_xpath('//input[@value="Login"]').click()
    context.test.assertEquals(context.selenium.title, "Social Network")


@given('I visit the scrape page')
def send_request_page(context):
    context.scrape_page = requests.get('http://127.0.0.1:8000/scrape')
    # assert context.scrape_page.status_code == 200


@then('I expect the response to be parsed as recipe')
def check_response_title_contains(context):
    context.selenium.get('http://127.0.0.1:8000/scrape')
    # current_url = 'http://127.0.0.1:8000/scrape'
    urlfield = context.selenium.find_element("name", "url")
    urlfield.send_keys(URL)
    submit = context.selenium.find_element("xpath", '//input[@value="Login"]')
    context.submit = submit.click()


@then('I expect the ingrdeients to not be empty')
def check_response_ingred_notempty(context):
    context.response = requests.get(URL)
    # recipe_site = context.selenium.get(URL)
    recipe_scrapes = scrape_html(html=context.response.text, org_url=URL)
    assert recipe_scrapes.ingredients() != ''
