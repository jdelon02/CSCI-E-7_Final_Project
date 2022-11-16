"""This is a docstring which describes the module"""
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, DetailView
from apps.login.models import User, UserFollowing 
from apps.recipes.models import Recipes
from apps.recipes.forms import recipesform


def login_view(request):
    """This is a docstring which describes the module"""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipesite/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipesite/login.html")


def logout_view(request):
    """This is a docstring which describes the module"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """This is a docstring which describes the module"""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipesite/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipesite/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipesite/register.html")
    
    
@csrf_exempt
@login_required
def followme(request, user_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        followed = data['followed']
        
        userCheck = get_object_or_404(User,pk=user_id)
        followCheck = UserFollowing.objects.all().filter(follower=user_id, following=followed)
        if followCheck:
            followUserCheck = get_object_or_404(followCheck)
            followUserCheck.delete()
            reply = 'Follow'
            liked=False
        else:
            follow = UserFollowing(
                follower = userCheck
            )
            follow.save()
            follow.following.add(followed)
            follow.save()
            
            reply = 'Unfollow'
            liked=True
            
        followerCount = UserFollowing.objects.all().filter(following=user_id).count()
        followedCount = UserFollowing.objects.all().filter(follower=user_id).count()
        
        # print(followerCount)
        # print(followedCount)

        return JsonResponse({'reply':reply, "followclass":liked, 'followerCount':followerCount, 'followedCount':f"{ followedCount }"})
    else:
        return HttpResponse('CSRF token is being exempted here!')

class UserDetailView(DetailView):
    """ 
    Leveraging django, but also had an issue with 
    having to rewrite queryset to pull twitterposts, 
    not user model. Then getting pager to work...  
    Good learning experience...
    """
    model = User
    context_object_name = 'user_detail'
    template_name = 'recipesite/user.html'
    # paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView,
                        self).get_context_data(*args, **kwargs)
        current_id = self.kwargs['pk']
        current_user = self.request.user.id
        context['currentUser'] = self.request.user.id
        allposts = Recipes.objects.all().filter(author=current_id).distinct().order_by('-id')
        context["allrecipes"] = allposts
        
        context['recipe_user'] = current_id
        
        paginator = Paginator(allposts,10)
        context['paginator'] = paginator
        
        page_number = self.request.GET.get('page')
        context['page_number'] = page_number
        
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        page = self.request.GET.get('page')
        context['page'] = page
        
        print(self.request)        
        
        followCheck = UserFollowing.objects.all().filter(follower=current_user, following=current_id)
        if followCheck.first():
            context['following'] = 'Unfollow'
        else:
            context['Following'] = "Follow"
            
        followerCount = UserFollowing.objects.all().filter(follower=current_id).exclude(following=current_id).count()
        print(followerCount)
        context['followerCount'] = followerCount  
        
        
        followedCount = UserFollowing.objects.all().filter(following=current_id).exclude(follower=current_id).count()
        print(followedCount)
        context['followedCount'] = followedCount  

        
        return context

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        this_user = User.objects.get(id=self.kwargs['pk'])
        this_userid = request.user.id
        this_user = User.objects.get(pk=this_userid)

        return HttpResponseRedirect(
            reverse_lazy(
                'user_detail', kwargs={
                    'pk': user_id}))

@csrf_exempt
@login_required
def like_button(request, post_id):
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


