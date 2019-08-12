from django.contrib import admin
from .models import Post, Email, Comment

admin.site.register(Post)
admin.site.register(Email)
admin.site.register(Comment)