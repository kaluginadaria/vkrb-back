from django.contrib import admin
from solo.admin import SingletonModelAdmin

from vkrb.feedback.models import InCharge, CategoryFeedback, FeedbackItem

admin.site.register(InCharge, SingletonModelAdmin)


@admin.register(CategoryFeedback)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(FeedbackItem)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'subject', 'text', 'created', 'is_seen')
    readonly_fields = ('created',)
    list_filter = ('is_seen', 'category')
    search_fields = ('author', 'category', 'subject')
