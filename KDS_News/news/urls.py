from django.contrib import admin
from django.urls import path, include
from news.views import *
from django.views.generic.base import TemplateView
from django.conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path('', index, name='home'),   
    path('signup/', signup , name='signup'),
    path('login/',Login,name='login'),
    path('logout', logout_view, name='logout'),
    path('<int:category_id>', Category_filter, name='Category'),
    path('Article/<int:article_id>', Article_view, name="Article"),
    path('profile/',profile_view,name="profile-view"),
    path('edit-profile/<int:profile_id>',edit_profile,name="edit-profile"),
    path('like/', like_post, name="like_post"),
    path('contact/',contact_view, name="contact"),
    path('delete', delete_profile_pic, name="delete_profile_pic" ),
    path('add-comment/<int:article_id>', add_comment, name="add-comment"),
    path('edit-article/<int:comment_id>', edit_comment, name="edit-comment" ),
    path('delete-article/<int:comment_id>', delete_comment, name="delete-comment" ),
    path('reply-comment/<int:article_id>', reply_comment, name="reply-comment")
]