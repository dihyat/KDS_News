from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#models = user, article, comment
class Category(models.Model):
    category_title = models.CharField(max_length=200, default="")


    def __str__(self):
        return self.category_title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_category = models.ManyToManyField(Category, blank = True)
    dob = models.DateField(auto_now=False, auto_now_add = False, null = True)
    
    user_pic = models.ImageField(upload_to = 'images/', blank = True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    Brief = models.TextField(max_length = 400)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #added for like
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    #user_comment = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)


    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment by {} on {}'.format(str(self.user), self.article)

  
