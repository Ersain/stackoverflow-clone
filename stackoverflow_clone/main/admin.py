from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

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
        'parent_link',
        'code',
        'post_type',
        'rating',
        'tags',
        'created_at',
        'updated_at',
    )
    exclude = ('parent',)

    def parent_link(self, obj):
        link = reverse('admin:main_post_change', args=[obj.parent.pk])
        return format_html(
            mark_safe(
                f'<b><a href="{link}" target="_blank">Parent - {obj.parent.code}</a></b>'
            )
        )

    parent_link.short_description = 'Parent'


admin.site.register(Tag)
