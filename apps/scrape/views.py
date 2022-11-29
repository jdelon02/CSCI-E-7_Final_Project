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
from apps.recipes.models import Recipe
from apps.login.models import User


class ScrapeFormView(View):
    form_class = ScrapeForm
    
    def get(self, request, *args, **kwargs):
        template_name = 'recipes/scrapetemplate.html'
        form = self.form_class()
        return render(request, template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        """This view is built using two different libraries.  
        One, the recipe_scraper lib to scrape/parse the webpage.
        Two, a "cloudsraper" library to get around cloudflare BOT/DDOS protection.
        This was necessary, since if you try to import a recipe more than once from
        (so far) food52.com, you get blocked."""
        
        form = self.form_class(request.POST)
        data = {}
        current_user = self.request.user.id
        
        if current_user:
            data['currentUser'] = current_user
            userLoad = User.objects.get(pk=current_user)
            print(userLoad)
        
        if form.is_valid():
            # <process form cleaned data>
            url = request.POST["url"]
            if url:
                data['url'] = url
                scraper = cloudscraper.create_scraper()
                if scraper:
                    recipe_scrapes = scraper.get(url).text
                    if recipe_scrapes:
                        recipe = scrape_html(html=recipe_scrapes, org_url=url)
                        
                        recipeScrape = Recipe()
                        recipeScrape.name = recipe.title()
                        if userLoad:
                            recipeScrape.author = userLoad
                        recipeScrape.save()
                        print(recipeScrape.id)
                    print(recipe.instructions)
                    attributes = dir(recipe)
                    # print(recipe.title())
                    # test = self.__ingredients(recipe.ingredients())
                    
                    # print(dir(recipe.ingredients()))
                    # print(f"{attributes}")
                    return HttpResponseRedirect('/recipe/' + str(recipeScrape.id))
    
    
    def __ingredients(ingredblob):
        print(ingredblob)
        return ''
    
    
    def __instructions(instrblob):
        pass