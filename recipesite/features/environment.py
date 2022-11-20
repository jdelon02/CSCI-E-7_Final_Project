from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
from django.core import management
from behave import *


def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    context.browser = webdriver.Remote(
        'http://192.168.86.12:4444/wd/hub',
        options=chrome_options,
    )
    context.base_url = "http://127.0.0.1:8000"


def before_scenario(context, scenario):
    pass


def after_all(context):
    # Quit our browser once we're done!
    context.browser.quit()
    context.browser = None
