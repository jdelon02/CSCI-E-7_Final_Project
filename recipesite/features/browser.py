from selenium import webdriver


class Browser(object):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        'http://192.168.86.12:4444/wd/hub',
        options=chrome_options,
    )

    def close(context):
        context.driver.close()

    def visit(context, location=''):
        base_url = "http://127.0.0.1:8000"
        context.driver.get(base_url + location)

    def query_selector_css(context, selector):
        element = context.driver.find_element_by_css_selector(selector)
        return element
