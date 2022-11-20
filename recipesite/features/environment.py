from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from behave import *
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipesite.settings')
django.setup()


def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    context.selenium = webdriver.Remote(
        'http://192.168.86.12:4444/wd/hub',
        options=chrome_options,
    )
    context.base_url = "http://127.0.0.1:8000"
    # context.test.assertEquals(context.selenium.title, "Site administration | Django site admin")


# def visit(context, location=''):
#     context.selenium.get(context.base_url + location)


# def after_all(context):
#     # Quit our browser once we're done!
#     context.selenium.close()
