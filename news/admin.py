from re import T
from django.contrib import admin
from .models import Editor, Tags, Article

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

# Register your models here.
admin.site.register(Editor)
admin.site.register(Tags)
admin.site.register(Article, ArticleAdmin)