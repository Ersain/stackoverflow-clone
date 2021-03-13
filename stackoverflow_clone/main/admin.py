from django.contrib import admin

from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = (
        'pk',
        'code'
    )

    list_filter = (
        'post_type',
    )

    list_display = (
        'pk',
        'post_type',
        'title',
        'author',
        'code',
    )

    autocomplete_fields = (
        'author',
    )

    readonly_fields = (
        'accepted_answer',
        'parent',
        'code',
        'post_type',
        'rating',
        'tags',
        'created_at',
        'updated_at',
    )


admin.site.register(Tag)
