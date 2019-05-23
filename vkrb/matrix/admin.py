# from django.contrib import admin, messages
# from mptt.admin import DraggableMPTTAdmin
#
# from vkrb.matrix.models import MatrixItem
#
#
# @admin.register(MatrixItem, )
# class MatrixAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
#     list_display = ('tree_actions', 'indented_title', 'title', 'text')
#     list_display_links = ('indented_title', 'text')
#     search_fields = ('title',)
#
#     def save_model(self, request, obj, form, change):
#         parent = form.cleaned_data['parent']
#         if parent is not None:
#             if parent.text in [None, ''] and parent.photo is None:
#                 super().save_model(request, obj, form, change)
#
#             else:
#                 messages.set_level(request, messages.ERROR)
#                 messages.error(request,
#                                "Вы не можете сохранить элемент таблицы"
#                                " компетенций, так как старший элемент "
#                                "уже имеет данные (фото или текст)")
#
#         else:
#             super().save_model(request, obj, form, change)
