from django.contrib import admin

from . models import Post
from .models import Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=('title','publish','created_at','status')
    list_filter=('publish','created_at')
    search_fields=('title','content')
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','created')
   
admin.site.register(Comment)