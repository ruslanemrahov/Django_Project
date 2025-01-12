from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' ,'publishingday' ,'slug']
    list_display_links = ['publishingday']
    list_editable = ['title']
    list_filter = ['publishingday']
    search_fields = ['title']

    class Meta:
        admin = Post

admin.site.register(Post ,PostAdmin)
