from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .managers import PublishedManager

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','DRAFT'
        PUBLISHED='PB','PUBLISHED'
    
    title=models.CharField(max_length=200)
    content=models.TextField()
    #author=models.CharField(max_length=50)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    slug=models.SlugField(unique_for_date='publish')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    publish=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=10,choices=Status.choices, default=Status.DRAFT)
    
    objects = models.Manager()  
    published = PublishedManager()  

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'id': self.id, 'year': self.created_at.year, 'month': self.created_at.month, 'date': self.created_at.day})

    class Meta:
        ordering = ['-publish']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='Comments'
)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
class Meta:
        ordering = ['created']
        
def __str__(self):
    return f'Comment by {self.name} on {self.post}'