from django.contrib import admin
from .models import Category, Event


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "location", "creator")
    list_filter = ("category", "date")
    search_fields = ("title", "description", "location")
    raw_id_fields = ("creator",)
