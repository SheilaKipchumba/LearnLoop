
from django.contrib import admin
from .models import Loop

class LoopAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']

admin.site.register(Loop)