"""This is a docstring which describes the module"""
import json
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.recipes.models import *
from apps.login.models.user import User
from apps.recipes.forms.ingredientsform import IngredientsForm
from apps.recipes.forms.recipesform import RecipesForm, IngredientFormSet, StepFormSet


paginationnum = 10


class Index(ListView):
    """This is a docstring which describes the module"""
    model = Recipes
    context_object_name = 'recipes_listview'
    template_name = 'recipesite/index.html'
    paginate_by = paginationnum

    def get_context_data(self, *args, **kwargs):
        context = super(Index,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user

        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            newquery = Recipes.objects.filter(name__contains=query).values_list('pk', flat=True)
            queryset = Recipes.objects.filter(pk__in=list(newquery))
        else:
            queryset = Recipes.objects.all().order_by('-id')
        return queryset


class BookmarkListView(UserPassesTestMixin, ListView):
    model = Recipes
    context_object_name = 'recipes_listview'
    template_name = 'recipesite/index.html'
    paginate_by = paginationnum

    def test_func(self):
        test = self.request.user.id
        if test:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super(BookmarkListView,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user
        context['bookmarks'] = True
        return context

    def get_queryset(self):
        current_user = self.request.user.id
        bookies = User.objects.filter(pk=current_user).values_list('userbookmarks', flat=True)
        queryset = Recipes.objects.filter(id__in=bookies).distinct().order_by('-id')
        return queryset

    def save_button(request, recipe_id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == "PUT":
                data = json.loads(request.body)
                postdata = data['user']
                recipe = Recipes.objects.get(pk=recipe_id)
                userLoad = User.objects.get(pk=postdata)
                usercheck = userLoad.userbookmarks.all()
                print(usercheck)
                if recipe in usercheck:
                    userLoad.userbookmarks.remove(Recipes.objects.get(pk=recipe_id))
                    userLoad.save()
                    print(userLoad)
                    saved = "Bookmark This"
                else:
                    userLoad.userbookmarks.add(Recipes.objects.get(pk=recipe_id))
                    userLoad.save()
                    print(userLoad)
                    saved = "Saved to Bookmarks"
                return JsonResponse({'saved': saved})
            else:
                return HttpResponse('CSRF token is being exempted here!')


class RecipeDetailView(DetailView):
    model = Recipes

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeDetailView,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user
        current_recipe = self.kwargs['pk']
        ingredientlist = Ingredients.objects.filter(recipe=current_recipe)
        ingredientlist = ingredientlist.all().order_by('id')
        context['ingredientlist'] = ingredientlist
        print(ingredientlist)
        steplist = Steps.objects.filter(recipe=current_recipe)
        steplist = steplist.all().order_by('id')
        context['steplist'] = steplist

        userLoad = User.objects.get(pk=current_user)
        usercheck = userLoad.userbookmarks.all()
        print(usercheck)
        thisrecipe = Recipes.objects.get(pk=current_recipe)
        print(thisrecipe)
        context['bookmark'] = "Bookmark Me"
        if thisrecipe in usercheck:
            context['bookmark'] = "Bookmark Saved"
        print(context['bookmark'])
        return context

    def like_button(request, recipe_id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == "PUT":
                data = json.loads(request.body)
                userdata = User.objects.get(pk=data['user'])
                postdata = data['id']
                postcheck = get_object_or_404(Recipes, pk=postdata)
                if postcheck.likes.filter(id=userdata.id):
                    postcheck.likes.remove(userdata)  # remove user from likes
                    liked = False
                else:
                    postcheck.likes.add(userdata)
                    liked = True
                return JsonResponse({'likes': postcheck.total_likes, "likeclass": liked})
            else:
                return HttpResponse('CSRF token is being exempted here!')

    def getRecipe(request, recipe_id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == "GET":
                print(recipe_id)
                postcheck = Recipes.objects.get(pk=recipe_id)
                userid = postcheck.user_id.id
                # print(userid)
                if postcheck:
                    jsonreply = postcheck.serialize()
                    return JsonResponse({"jsonreply": jsonreply, "id": userid})
                else:
                    pass
            elif request.method == "PUT":
                data = json.loads(request.body)
                print(data)
                # postdata = User.objects.get(username=data['user'])
                # postdata = data['id']
                postcheck = get_object_or_404(Recipes, pk=recipe_id)
                if postcheck:
                    postcheck.body = data
                    postcheck.save()
                    return JsonResponse(postcheck.serialize())
            else:
                return HttpResponse('CSRF token is being exempted here!')

    # def get_queryset(self):
    #     current_user = self.request.user.id
    #     ingredients = UserFollowing.objects.filter(follower_id=current_user).values_list('following', flat=True)
    #     queryset = Recipes.objects.filter(author_id__in=followIDs).distinct().order_by('-id')
    #     return queryset


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipes
    form_class = RecipesForm
    template_name = 'recipesite/recipes_edit.html'

    def test_func(self):
        test = self.request.user.id
        if test:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredientformset = IngredientFormSet()
        stepformset = StepFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredientformset=ingredientformset,
                                  stepformset=stepformset
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredientformset = IngredientFormSet(data=self.request.POST,
                                              instance=self.object)
        stepformset = StepFormSet(data=self.request.POST,
                                  instance=self.object)
        if form.is_valid() and ingredientformset.is_valid() and stepformset.is_valid():
            return self.form_valid(form, ingredientformset, stepformset)
        else:
            return self.form_invalid(form, ingredientformset, stepformset)

        # self.object = self.get_object()
        # form = RecipesForm(data=self.request.POST, instance=self.object)
        # ingredientformset = IngredientFormSet(data=self.request.POST,
        #      instance=self.object)
        # stepformset = StepFormSet(data=self.request.POST,
        #      instance=self.object)
        # if form.is_valid() and ingredientformset.is_valid() and stepformset.is_valid():
        #     return self.form_valid(form, ingredientformset, stepformset)
        # else:
        #     return self.form_invalid(form, ingredientformset, stepformset)

    def form_valid(self, form, ingredientformset, stepformset):
        print(form.instance)
        recipe = form.save(commit=False)
        recipe.author = self.request.user

        if form.data['servingQuantity'] == '':
            recipe.servingQuantity = None

        if form.data['skillLevel'] == '':
            recipe.skillLevel = None

        if form.data['prepHour'] == '':
            recipe.prepHour = None

        if form.data['prepMin'] == '':
            recipe.prepMin = None

        if form.data['cookHour'] == '':
            recipe.cookHour = None

        if form.data['cookMin'] == '':
            recipe.cookMin = None

        if 'recipe_img' in form.files:
            recipe.recipe_img = form.files['recipe_img']

        print(recipe)

        recipe.save()

        ingredientlist = ingredientformset.save(commit=False)
        for ingr in ingredientlist:
            print(ingr)
            if ingr.name:
                ingr.recipe = recipe
                ingr.save()
            else:
                new_ingr = Ingredients()
                new_ingr.recipe = recipe
                new_ingr.name = ingr.instance.name
                new_ingr.description = ingr.instance.description
                new_ingr.quantityfraction = ingr.instance.quantityfraction
                new_ingr.quantitywhole = ingr.instance.quantitywhole
                new_ingr.unitId = ingr.instance.unitId
                new_ingr.save()

        steplist = stepformset.save(commit=False)
        for step in steplist:
            step.recipe = recipe
            step.step = step.step
            step.save()

        return HttpResponseRedirect(
            reverse_lazy('bookmarks'))

    def form_invalid(self, form, ingredientformset, stepformset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredientformset=ingredientformset,
                                  stepformset=stepformset
                                  )
        )


class RecipeUpdateView(UpdateView):
    model = Recipes
    # fields = '__all__'
    form_class = RecipesForm
    formset_class = {
        'ingredientformset': IngredientFormSet,
        'stepformset': StepFormSet
    }
    template_name = 'edit.html'
    template_name = 'recipesite/recipes_edit.html'

    def test_func(self):
        test = self.request.user.id
        if test:
            return True
        else:
            return False

    # def get_context_data(self, **kwargs):
    #     context = super(RecipeUpdateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['ingredientformset'] = IngredientFormSet(self.request.POST, instance=self.object)
    #         context['stepformset'] = StepFormSet(self.request.POST, instance=self.object)
    #         # context['formset'].full_clean()
    #     else:
    #         context['ingredientformset'] = IngredientFormSet(instance=self.object)
    #         context['stepformset'] = StepFormSet(instance=self.object)
    #     return context

    def get_object(self, queryset=None):
        self.object = super(RecipeUpdateView, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        ingredientformset = IngredientFormSet(instance=self.object)
        stepformset = StepFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=RecipesForm(instance=self.object),
                                  ingredientformset=ingredientformset,
                                  stepformset=stepformset
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RecipesForm(data=self.request.POST, instance=self.object)
        ingredientformset = IngredientFormSet(data=self.request.POST,
                                              instance=self.object)
        stepformset = StepFormSet(data=self.request.POST,
                                  instance=self.object)
        if form.is_valid() and ingredientformset.is_valid() and stepformset.is_valid():
            return self.form_valid(form, ingredientformset, stepformset)
        else:
            return self.form_invalid(form, ingredientformset, stepformset)

    def form_valid(self, form, ingredientformset, stepformset):
        recipe = form.save(commit=False)

        if form.data['servingQuantity'] == '':
            recipe.servingQuantity = None
        else:
            recipe.servingQuantity = form.data['servingQuantity']

        if form.data['skillLevel'] == '':
            recipe.skillLevel = None
        else:
            recipe.skillLevel = form.data['skillLevel']

        if form.data['prepHour'] == '':
            recipe.prepHour = None
        else:
            recipe.prepHour = form.data['prepHour']

        if form.data['prepMin'] == '':
            recipe.prepMin = None
        else:
            recipe.prepMin = form.data['prepMin']

        if form.data['cookHour'] == '':
            recipe.cookHour = None
        else:
            recipe.cookHour = form.data['cookHour']

        if form.data['cookMin'] == '':
            recipe.cookMin = None
        else:
            recipe.cookMin = form.data['cookMin']

        if 'recipe_img' in form.files:
            recipe.recipe_img = form.files['recipe_img']

        print(recipe)

        recipe.save()

        ingredients = ingredientformset
        # ingredients.save(commit=False)
        print(ingredients)
        for ingr in ingredients:
            print(ingr)
            if ingr.instance.name:
                ingr.recipe = recipe
                ingr.save()
            else:
                new_ingr = Ingredients()
                new_ingr.recipe = recipe
                new_ingr.name = ingr.instance.name
                new_ingr.description = ingr.instance.description
                new_ingr.quantityfraction = ingr.instance.quantityfraction
                new_ingr.quantitywhole = ingr.instance.quantitywhole
                new_ingr.unitId = ingr.instance.unitId
                new_ingr.save()

        steplist = stepformset
        for step in steplist:
            step.recipe = recipe
            step.step = step.instance.step
            step.save()

        return HttpResponseRedirect(
            reverse_lazy('recipedetail', kwargs={'pk': recipe.id}))

    def form_invalid(self, form, ingredientformset, stepformset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredientformset=ingredientformset,
                                  stepformset=stepformset
                                  )
        )
