from django.contrib import admin
from .models import *


class CategorysAdmin(admin.ModelAdmin):
    list_display = ('name_category',)


admin.site.register(Author)
admin.site.register(Category, CategorysAdmin)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
