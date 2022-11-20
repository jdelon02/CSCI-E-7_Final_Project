from behave import *


@given('today is "{day}"')
def today(context, day):
    context.sunday = day
    assert True


@when('I ask whether it\'s "{day}" yet')
def nottoday(context, day):
    context.day_asked = day
    assert True


@then('I should be told "{text}"')
def is_day_other_day(context, text):
    assert context.day_asked != context.sunday, True
