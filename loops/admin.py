"""from django.contrib import admin
from .models import Loop, Like, Comment

# Register your models here.

class LoopAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']

admin.site.register(Loop)


@admin.register(Loop)
class LoopAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'difficulty', 'is_premium', 'created_at']
    list_filter = ['category', 'difficulty', 'is_premium', 'created_at']
    search_fields = ['title', 'description', 'content']
    date_hierarchy = 'created_at'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'loop', 'created_at']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'loop', 'created_at']
    list_filter = ['created_at']"""
from django.contrib import admin
from .models import Loop

class LoopAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']

admin.site.register(Loop)