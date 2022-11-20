# features/steps/scrape_test.py
import requests
from behave import *
from recipe_scrapers import scrape_me, scrape_html
from selenium.webdriver.common.by import By


URL = 'https://www.foodnetwork.com/recipes/tyler-florence/cranberry-orange-sauce-recipe3-1946636'
TEXT = 'Cranberry-Orange Sauce'
NEWURL = ''


@given('I log into the site login')
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


@then('I should visit homepage')
def visit_home(context):
    context.selenium.get('http://127.0.0.1:8000/')
    context.test.assertEquals(context.selenium.title, "Social Network")
