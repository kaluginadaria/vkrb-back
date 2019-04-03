from django.contrib import admin

from vkrb.attachment.models import Attachment

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

