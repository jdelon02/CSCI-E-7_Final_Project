"""This is a docstring which describes the module"""
import json
import re
from urllib.parse import urlparse
import requests
import cloudscraper
from recipe_scrapers import scrape_me, scrape_html
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views import View
from apps.scrape.forms import ScrapeForm


def Index(request):
    """This view is built using two different libraries.  
    One, the recipe_scraper lib to scrape/parse the webpage.
    Two, a "cloudsraper" library to get around cloudflare BOT protection.
    This was necessary, since if you try to import a recipe more than once from
    (so far) food52.com, you get blocked."""
    if request.method == "POST":
        data = []

        # Just a quick check
        url = request.POST["url"]
        if url:
            data.append(url)
            scraper = cloudscraper.create_scraper()
            if scraper:
                recipe_scrapes = scraper.get(url).text
                if recipe_scrapes:
                    recipe = scrape_html(html=recipe_scrapes, org_url=url)
                # print(vars(recipe))
                attributes = dir(recipe)
                print(recipe.title())
                print(recipe.instructions())
                print(attributes)

        # https://food52.com/recipes/88304-buttermilk-marinated-roast-chicken-from-samin-nosrat
        # http://feeds.feedburner.com/food52-TheAandMBlog

        return render(request, "recipes/scrape_review.html", {'data': data})
    else:
        return render(request, "recipes/scrapetemplate.html")
