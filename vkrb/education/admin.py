from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from vkrb.education.models import (
    InternalEducation,
    CategoryInternalEducation,
    CategoryLibrary,
    CategoryCatalog,
    CatalogItem,
    Reduction,
    ScienceArticle, Literature)

#
# class CategoryCatalogInline(SortableInlineAdminMixin, admin.StackedInline):
#     model = CategoryCatalog
#     extra = 0


# class ReductionInline(SortableInlineAdminMixin, admin.StackedInline):
#     model = Reduction
#     extra = 0
#
#
# @admin.register(Reduction)
# class ReductionAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('reduction', 'transcript', 'library')
#     search_fields = ('reduction', 'transcript')
#     list_filter = ('library',)


# @admin.register(InternalEducation)
# class InternalEducationAdmin(admin.ModelAdmin):
#     list_display = ('title', 'type', 'location', 'image_tag')
#     search_fields = ('title', 'location')
#     list_filter = ('type', 'location')
#
#
# @admin.register(CategoryInternalEducation)
# class CategoryInternalEducationAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('title',)
#     search_fields = ('title',)
#
#
# @admin.register(CategoryLibrary)
# class CategoryLibraryAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('title',)
#     search_fields = ('title',)
#     inlines = [CategoryCatalogInline, ReductionInline]

#
# @admin.register(CategoryCatalog)
# class CategoryCatalogAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('title', 'library')
#     search_fields = ('title',)
#
#
# @admin.register(CatalogItem)
# class CatalogItemAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('title', 'type', 'image_tag')
#     search_fields = ('title', 'location')
#     list_filter = ('type',)


@admin.register(ScienceArticle)
class ScienceArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'photo')
    search_fields = ('title',)
    list_filter = ('library',)
    fields = ('title', 'photo', 'author', 'body', 'date_of_issued', 'attachment')


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'image_tag')
    search_fields = ('title', )
    exclude = ('library','keywords')
