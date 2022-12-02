"""This is a docstring which describes the module"""
import json
import re
from bs4 import BeautifulSoup
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
from apps.recipes.models import Recipe, Step, Ingredient
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
            # print(userLoad)

        if form.is_valid():
            # <process form cleaned data>
            url = request.POST["url"]
            if url:
                data['url'] = url
                scraper = cloudscraper.create_scraper()
                if scraper:
                    recipe_scrapes = scraper.get(url).text
                    if recipe_scrapes:
                        recipe = ''
                        try:
                            recipe = scrape_html(html=recipe_scrapes, org_url=url)
                        except:
                            try:
                                recipe = scrape_me(url, wild_mode=True)
                            except:
                                return HttpResponseRedirect(reverse_lazy('index'))
                            
                    
                        if recipe != '':

                            # Custom Scraper for Prep Time and Cook Time.  Default is "total time"
                            # But I want the separate info.
                            soup = BeautifulSoup(recipe_scrapes, "html.parser")

                            recipeScrape = Recipe()
                            recipeScrape.name = recipe.title()

                            try:
                                prepTime = soup.find(text="Prep time").next_element.text
                                if prepTime:
                                    prepTime = prepTime.strip().lower()
                                    prepMin = self.__splitTime(prepTime, "minutes")
                                    if prepMin:
                                        recipeScrape.prepMin = prepMin
                                    prepHour = self.__splitTime(prepTime, "hour")
                                    if prepHour:
                                        recipeScrape.prepHour = int(prepHour)
                            except:
                                pass

                            try:
                                cookTime = soup.find(text="Cook time").next_element.text
                                if cookTime:
                                    cookTime = cookTime.strip().lower()
                                    cookMin = self.__splitTime(cookTime, "minutes")
                                    if cookMin:
                                        recipeScrape.cookMin = cookMin
                                    cookHour = self.__splitTime(cookTime, "hour")
                                    if cookHour:
                                        print(True)
                                        print(cookHour)
                                        recipeScrape.cookHour = int(cookHour)
                            except:
                                pass

                            try:
                                totalTime = recipe.total_time()
                                print(totalTime)
                            except:
                                pass

                            try:
                                cuisine = recipe.cuisine()
                                self.__prepTime(cuisine)
                            except NotImplementedError:
                                pass

                            try:
                                category = recipe.category()
                                self.__prepTime(category)
                            except NotImplementedError:
                                pass

                            if userLoad:
                                recipeScrape.author = userLoad
                            recipeScrape.save()

                            scrapeInstructions = recipe.instructions().splitlines()

                            # Let's save the instructions as steps.
                            self.__stepSave(scrapeInstructions, recipeScrape)

                            ingrList = recipe.ingredients()
                            self.__ingrSave(ingrList, recipeScrape)

                            return HttpResponseRedirect('/recipe/' + str(recipeScrape.id))

    def __break_up_string_number(self, ingr):
        units = (
            'cup',
            'tablespoon',
            'tablespoons',
            'teaspoon',
            'pint',
            'quart',
            'ounce',
            'dozen',
            'can',
            'bunch',
            'whole',
        )
        # set some defaults.
        results = {}
        results['whole'] = ''
        results['fraction'] = ''
        results['unit'] = ''
        results['name'] = ''
        results['description'] = ''

        first_digit = ingr.split(" ", 1)
        if first_digit[0].isdigit():
            results['whole'] = first_digit[0]
        else:
            match = re.findall("\d+\/\d+", first_digit[0])
            if match:
                results['fraction'] = first_digit[0]
            elif first_digit[0].lower() in units:
                results['unit'] = str(first_digit[0])
            else:
                commacheck = re.findall(",", ingr)
                if commacheck:
                    namesplit = ingr.split(",", 1)
                    if namesplit:
                        results['name'] = str(namesplit[0])
                        results['description'] = str(namesplit[1])
                else:
                    results['name'] = ingr
        if results['name'] == '':
            second_digit = first_digit[1].split(" ", 1)
            match = re.findall("\d+\/\d+", second_digit[0])
            if match:
                results['fraction'] = second_digit[0]
            elif second_digit[0].lower() in units:
                results['unit'] = str(second_digit[0])
            else:
                commacheck = re.findall(",", second_digit[1])
                if commacheck:
                    namesplit = second_digit[1].split(",", 1)
                    if namesplit:
                        if namesplit[0].lower() in units:
                            results['unit'] = str(namesplit[0])
                        else:
                            results['name'] = str(namesplit[0])
                            results['description'] = str(namesplit[1])
                else:
                    results['name'] = str(first_digit[1])
            if results['name'] == '':
                commacheck = re.findall(",", second_digit[1])
                if commacheck:
                    namesplit = second_digit[1].split(",", 1)
                    results['name'] = str(namesplit[0])
                    results['description'] = str(namesplit[1])
                else:
                    results['name'] = str(second_digit[1])

        return results

    def __ingrSave(self, ingrList, recipeScrape):
        for ingr in ingrList:
            # Time to scrap to separate.
            results = self.__break_up_string_number(str(ingr))
            # print(results)
            new_ingr = Ingredient()
            new_ingr.quantitywhole = results['whole']
            new_ingr.quantityfraction = results['fraction']
            new_ingr.unitId = results['unit']
            new_ingr.recipe = recipeScrape
            new_ingr.name = results['name']
            new_ingr.description = results['description']
            new_ingr.save()

    def __stepSave(self, scrapeInstructions, recipeScrape):
        for instr in scrapeInstructions:
            singleStep = Step()
            singleStep.recipe = recipeScrape
            singleStep.step = instr
            singleStep.save()

    def __cuisine(self, cuisine):
        print(cuisine)
        pass

    def __category(self, category):
        print(category)
        pass

    def __splitTime(self, timestring, method):
        print(method)

        timesplit = timestring.split(":", 1)
        if len(timesplit) > 1:
            if method == 'minutes':
                results = timesplit[1].isdigit()
                return results
            else:
                results = timesplit[0].isdigit()
                return results

        if re.search(method, timestring):
            results = re.findall(r"\d+", timestring)
            results = ''.join(map(str, results))
            return results
