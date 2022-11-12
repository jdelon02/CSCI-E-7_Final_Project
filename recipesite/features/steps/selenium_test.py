# examples/selenium-requests/features/steps/selenium_steps.py
from behave import *
from urllib.parse import urljoin
import requests


@given('I send a {method} request to the page "{page}"')
def send_request_page(context, method, page):
    url = urljoin(context.base_url, page)
    context.response = requests.get(url)
    
@then('I expect the response text contains "{text}"')
def check_response_text_contains(context, text):
    assert text in context.response.text