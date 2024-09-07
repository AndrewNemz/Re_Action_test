from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'post_name',
        'post_text',
        'created',
        'post_status'
    )
    search_fields = ('post_name',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
