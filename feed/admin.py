from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")
    search_fields = ("author__username", "content")
