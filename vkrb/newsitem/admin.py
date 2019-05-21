from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin

from vkrb.client.push import NewNewsItemPush
from vkrb.newsitem.forms import NewsItemAttachmentAdminForm, NewsForm
from vkrb.newsitem.models import NewsItem, CategoryNewsItem


class AttachmentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = NewsItem.attachments.through
    extra = 0
    formset = NewsItemAttachmentAdminForm


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_tag',)
    inlines = (AttachmentsInline,)
    fields = ('category', 'title', 'text', 'image_tag', 'keywords', 'created')
    list_filter = ('category',)
    search_fields = ('title', 'text')
    readonly_fields = ('image_tag',)
    form = NewsForm

    def save_model(self, request, obj, form, change):
        newsitem = super().save_model(request, obj, form, change)
        # if change is False:
        #     NewNewsItemPush(obj).send()


@admin.register(CategoryNewsItem)
class CategoryNewsItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
