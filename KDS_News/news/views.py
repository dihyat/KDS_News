from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import QueryDict


from .models import Article, Category, Profile, Comment

import os, datetime

from .forms import LoginForm, SignUpForm, ProfileForm, CommentForm

#Handles signing up of a user


def signup(request):
    form = SignUpForm(request.POST)
    post_dict = request.POST
    if request.method == 'POST':
        if form.is_valid():

            #retriving data from request.POST
            date_obj = datetime.datetime(
                int(post_dict['dob_year']),
                int(post_dict['dob_month']),
                int(post_dict['dob_day'])
                )

            #creating user
            user = User.objects.create_user(
                username = str(post_dict['username']),
                first_name = str(post_dict['first_name']),
                last_name = str(post_dict['last_name']),
                email =  str(post_dict['email']),
                password = str(post_dict['password1'])
                )

            #adding dob to profile
            profile = get_object_or_404(Profile, user = user)
            profile.dob = date_obj
            profile.save()

            #login
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)

            #email
            Email_content = render_to_string('Email.html', {}, request = request)
            #building email object
            email = EmailMessage(
                "Welcome to KDS_News",
                Email_content,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.fail_silently = False
            email.send()
            return redirect(index)
        else:
            return render(request, 'signup.html', {'form': form, "is_signup": True})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form, "is_signup": True})
def Login(request):
    if request.method == "POST":
        login_form = LoginForm(data=request.POST or None)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Redirect to a success page.
                login(request, user)
                return redirect(index)
                
            else:
                # Return an 'invalid login' error message.
                return render(request, "login.html", {"form":login_form, "is_login": True})
        else:
            return render(request, "login.html", {"form":login_form, "is_login": True})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'form' : login_form, "is_login": True})

@require_http_methods(["GET"])
@login_required
def index(request):
    articles = []
    profile = get_object_or_404(Profile, id = request.user.profile.id)
    categories = profile.favourite_category.all()

    if len(categories) < len(Category.objects.all()) and len(categories) >0 :
        tmp_articles = []
        for category in categories:
            tmp_articles = list(Article.objects.filter(article_category=category))
            for article in tmp_articles:
                articles.append(article)
    else:
        categories = []
        articles = Article.objects.values()
        for article in articles:
            categories.append(get_object_or_404(Category, id = article['article_category_id']))

    zip_articles = zip(articles, categories)

    context = {
        "Articles": zip_articles,
        "title" : "Home",
        "categories": set(categories)
    }
    return render(request, 'home.html',context)

def logout_view(request):
    logout(request)
    return redirect(Login)
    # Redirect to a success page.

@require_http_methods(["GET"])
@login_required
def Category_filter(request, category_id):
    profile = get_object_or_404(Profile,id = request.user.profile.id)
    profile_categories = get_categories(profile)
    
    Articles = Article.objects.values()
    categories = []
    list_Articles = []
    for article in Articles:
        if(category_id == article['article_category_id']):
            categories.append(get_object_or_404(Category, id = article['article_category_id']).category_title)
            list_Articles.append(article)
    Articles = zip(list_Articles,categories)
    return render(request, 'home.html',{"Articles": Articles, "title" : categories[0], "categories": profile_categories})
@require_http_methods(["GET"])
@login_required
def Article_view(request, article_id):
    profile = get_object_or_404(Profile, user = request.user)
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article, reply=None).order_by('-id')
    categories = get_categories(profile)
    #this part handles like functionality
    total_likes = article.total_likes()
    is_liked = True
    if(len(article.likes.all().filter(id = request.user.id)) == 0):
        is_liked = False
    #creating teh context to be sent in render
    context = {
        "article" : article,
        "category" : article.article_category.category_title,
        "categories": categories,
        "comments" : comments,
        "comment_form":CommentForm(),
        "total_likes" : total_likes,
        "is_liked": is_liked,
    }
    return render(request,"Article.html", context)

@require_http_methods(["GET"])
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile,user=request.user)
    categories = get_categories(profile)
    profile_form = ProfileForm()
    context = {
        "profile" : profile,
        "profile_form": profile_form,
        "categories": categories,
    }
    return render(request, "profile.html",context)

@require_http_methods(["POST"])
@login_required
def edit_profile(request,profile_id):
    profile = get_object_or_404(Profile,user = request.user)
    profile_form = ProfileForm(data = request.POST, files = request.FILES)
    if profile_form.is_valid():
        profile.favourite_category.clear()
        profile.save()
        favourite_categories = request.POST.getlist('favourite_category')
        for fav_cat in favourite_categories:
            profile.favourite_category.add(get_object_or_404(Category, id = fav_cat))
            profile.save()
        if profile_form.cleaned_data["user_pic"] != None:
            image_path = settings.MEDIA_ROOT + '/' + profile.user_pic.name
            if os.path.isfile(image_path):
                os.remove(image_path)
            profile.user_pic = profile_form.cleaned_data["user_pic"]
            profile.save()
        
        return redirect(profile_view)
    else:
        return render(request, "Error.html",{"error": profile_form.errors })

#handles like

@login_required
@require_http_methods(["PUT"])
def like_post(request):
    data = QueryDict(request.body)
    article = get_object_or_404(Article, id=data['id'])
    is_liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        is_liked = False
    else:
        article.likes.add(request.user)
        is_liked = True
    context = {
        'article' : article,
        'is_liked' : is_liked,
        'total_likes': article.total_likes(),
    }
    html = render_to_string('like.html',context, request=request)
    return JsonResponse({'form': html})
@require_http_methods(["DELETE"])
@login_required
def delete_profile_pic(request):
    id = request.user.profile.id
    profile = get_object_or_404(Profile, id = id)
    image_path = settings.MEDIA_ROOT + '/' + profile.user_pic.name
    if os.path.isfile(image_path):
        os.remove(image_path)   
    profile.user_pic = None
    profile.save() 
    return JsonResponse({},status=200)
@require_http_methods(["PUT"])
@login_required
def edit_comment(request, comment_id):
    data = QueryDict(request.body)
    form = CommentForm(data)
    if form.is_valid():
        comment = get_object_or_404(Comment, id = comment_id)
        comment.content = form.cleaned_data['content']
        comment.save()
        return JsonResponse({"content": comment.content},status = 200)
    else:
        return JsonResponse({}, status = 404)

@require_http_methods(["DELETE"])
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    comment.delete()
    return JsonResponse({},status = 200)
@require_http_methods(["POST"])
@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article_id, reply=None).order_by('-id')
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        content = comment_form.cleaned_data['content']
        comment = Comment.objects.create(article=article , user=request.user, content=content, reply=None)
        comment.save()
        html = render_to_string('comment.html', {"article" : article, "comments" : comments, "comment_form":comment_form}, request=request)
        return JsonResponse({'form': html}, status = 200)
    else:
        return JsonResponse({},status = 404)

@require_http_methods(["POST"])
@login_required
def reply_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article_id, reply=None).order_by('-id')
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        content = comment_form.cleaned_data['content']
        replyId = request.POST['comment_id']
        reply_query = get_object_or_404(Comment,id = replyId)
        comment = Comment.objects.create(article=article , user=request.user, content=content, reply=reply_query)
        comment.save()
        html = render_to_string('comment.html', {"article" : article, "comments" : comments, "comment_form":comment_form}, request=request)
        return JsonResponse({'form': html}, status = 200)
    else:
        return JsonResponse({},status = 404)

@require_http_methods(['GET'])
def contact_view(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user = request.user)
        categories = get_categories(profile)
        return render(request, 'contact.html', {'categories': categories, "is_contact": True})
    else:
        return render(request, 'contact.html', {"is_contact": True})

def get_categories(profile):
    categories = profile.favourite_category.all()
    if len(categories)==0:
        categories = Category.objects.all()
    return categories
