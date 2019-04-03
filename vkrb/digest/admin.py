from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin

from vkrb.digest.models import (
    DigestCategory,
    Digest,
    Article
)


@admin.register(Digest)
class DigestAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)


class AttachmentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Article.attachments.through
    extra = 0
    readonly_fields = ('image_tag',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [AttachmentsInline]

    list_display = ('title', 'digest')
    list_filter = ('digest', 'digest__category')
    search_fields = ('title', 'body')


@admin.register(DigestCategory)
class DigestCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
