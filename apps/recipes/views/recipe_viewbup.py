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
from recipesite.models import *
from recipesite.forms import ingredientsform, recipesform
from recipesite.forms.recipesform import RecipesForm, IngredientFormSet


paginationnum = 10


class Index(ListView):
    """This is a docstring which describes the module"""
    model = Recipes
    context_object_name = 'recipe_listview'
    template_name = 'recipesite/index.html'
    paginate_by = paginationnum
    
    def get_context_data(self, *args, **kwargs):
        context = super(Index,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user
        
        return context
    
    def get_queryset(self):
        queryset = Recipes.objects.all().order_by('-id')
        return queryset
    
class BookmarkListView(UserPassesTestMixin, ListView):
    model = Recipes
    context_object_name = 'recipes_listview'
    template_name = 'recipesite/following.html'
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
        return context
    
    def get_queryset(self):
        current_user = self.request.user.id
        followIDs = UserFollowing.objects.filter(follower_id=current_user).values_list('following', flat=True)
        queryset = Recipes.objects.filter(author_id__in=followIDs).distinct().order_by('-id')
        return queryset


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipes
    form_class = RecipesForm
    template_name = 'recipesite/recipes_form.html'
    
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
        formset = IngredientFormSet()
        return self.render_to_response(
                self.get_context_data(form=form,
                        formset=formset,
                                )
                        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormSet(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        # print(form.instance)
        recipe = form.save(commit=False)
        # print(form.data)
        recipe.author = self.request.user
        recipe.servingQuantity = ServingSize.objects.create(serving=form.data['servingQuantity'])
        recipe.skillLevel = Difficulty.objects.create(level=form.data['skillLevel'])
        recipe.prepmin = PrepCookMin.objects.create(timeMin=form.data['prepmin'])
        recipe.prephour = PrepCookHour.objects.create(timeHour=form.data['prephour'])
        recipe.cookmin = PrepCookMin.objects.create(timeMin=form.data['cookmin'])
        recipe.cookhour = PrepCookHour.objects.create(timeHour=form.data['cookhour'])        
        recipe.save()
        # print(recipe.pk)

        ingredientlist = formset.save(commit=False)
        for ingr in ingredientlist:
            ingr.instance = self.object
            ingr.recipe_id = recipe.pk
            # print(ingr.instance)
            ingr.save()
            # print(ingr)
        return HttpResponseRedirect(
                reverse_lazy('recipe-add'))
        

class RecipeUpdateView(UpdateView):
    model = Recipes
    fields = ['name']
    def test_func(self):
        test = self.request.user.id
        if test:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeUpdateView,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user  
        return context



@csrf_exempt
@login_required
def like_button(request, recipe_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        userdata = User.objects.get(username=data['user'])
        postdata = data['id']
        postcheck=get_object_or_404(Recipes,pk=postdata)
        if postcheck.likes.filter(id=userdata.id):
            postcheck.likes.remove(userdata) #remove user from likes 
            liked=False
        else:
            postcheck.likes.add(userdata)
            liked=True
        return JsonResponse({'likes':postcheck.total_likes, "likeclass":liked})
    else:
        return HttpResponse('CSRF token is being exempted here!')

# class RecipeDeleteView(DeleteView):
#     model = Recipes
#     success_url = reverse_lazy('recipe-list')


class RecipeDetailView(DetailView):
    # specify the model to use
    model = Recipes
    context_object_name = 'recipe_detail'
  
    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(RecipeDetailView,
             self).get_context_data(*args, **kwargs)
        print(self)
        # add ingredients
        ingredients = Ingredients.objects.get(recipe=kwargs['object'].pk)
        print(ingredients)
        context["ingredients"] = "ingredients"        
        return context

    
# def single_recipe(request):
#     """This is a docstring which describes the module"""
#     if request.method == "GET":
#         template_name = 'recipesite/add.html'
#         form = recipesform.RecipesForm()
#         ingredientformset = IngredientFormSet
#         # bid_class = self.bid_class
#         return render(request, template_name, {'form': form, 'ingredientformset': ingredientformset})

#     elif request.method == "POST":
#         form = recipesform(request.POST)
#         current_userid = request.user.id
#         current_user = User.objects.get(pk=current_userid)
#         if form.is_valid():
#             # new_post = Recipes()
#             # new_post.body = form.data['body']
#             # new_post.user_id = current_user
#             # new_post.save()
#             # form.save()
#             # messages.add_message(request, messages.SUCCESS, 
#                                 # 'Post Added.')
#             return HttpResponseRedirect(
#                 reverse_lazy('addpost'))
#         else:
#             # messages.add_message(
#             #     request,
#             #     messages.ERROR,
#             #     'Post Not Added.')
#             return render(request, template_name, {'form': form})

# @csrf_exempt
# @login_required
# def single_recipe(request):
#     """This is a docstring which describes the module"""
#     if request.method == "GET":
#         template_name = 'recipes/recipesingle_form.html'
#         form = Recipes()
#         # bid_class = self.bid_class
#         return render(request, template_name, {'form': form})

    # elif request.method == "POST":
    #     form = RecipesForm(request.POST)
    #     current_userid = request.user.id
    #     current_user = User.objects.get(pk=current_userid)
    #     if form.is_valid():
    #         new_recipe = Recipes()
    #         new_recipe.description = form.data['decription']
    #         new_recipe.user_id = current_user
    #         new_recipe.save()
    #         # form.save()
    #         messages.add_message(request, messages.SUCCESS, 
    #                             'Post Added.')
    #         return HttpResponseRedirect(
    #             reverse_lazy('addpost'))
    #     else:
    #         messages.add_message(
    #             request,
    #             messages.ERROR,
    #             'Post Not Added.')
    #         return render(request, template_name, {'form': form})


@csrf_exempt
def getRecipe(request, recipe_id):
    if request.method == "GET":
        print(recipe_id)
        postcheck=Recipes.objects.get(pk=recipe_id)
        userid = postcheck.user_id.id
        # print(userid)
        if postcheck:
            jsonreply = postcheck.serialize()
            return JsonResponse({"jsonreply":jsonreply, "id":userid})
        else:
            pass
    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        # postdata = User.objects.get(username=data['user'])
        # postdata = data['id']
        postcheck=get_object_or_404(Recipes,pk=recipe_id)
        if postcheck:
            postcheck.body = data
            postcheck.save()
            return JsonResponse(postcheck.serialize())
    else:
        return HttpResponse('CSRF token is being exempted here!')
