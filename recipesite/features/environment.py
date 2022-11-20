from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
from django.core import management
from behave import *
from browser import Browser
from steps.pageobjects.login import LoginPage


def before_all(context):
    context.browser = Browser()
    context.base_url = "http://127.0.0.1:8000"
    context.signin = LoginPage()


def before_scenario(context, scenario):
    pass


def after_all(context):
    # Quit our browser once we're done!
    context.signin.log_out()
    context.browser.close()
    context.browser = None
