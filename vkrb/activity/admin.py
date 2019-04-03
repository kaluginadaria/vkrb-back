from django.contrib import admin

from vkrb.activity.models import GiItem, SiItem


@admin.register(GiItem)
class GiItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

    search_fields = ('title', 'description')
    exclude = ('is_actual',)

    def get_queryset(self, request):
        qs = super(GiItemAdmin, self).get_queryset(request)
        return qs.filter(is_actual=True)


@admin.register(SiItem)
class SiItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'gi')
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        if not form.cleaned_data.get('gi'):
            gi, _ = GiItem.objects.get_or_create(title='Отсутствует',
                                                 is_actual=False)
            obj.gi = gi
        super().save_model(request, obj, form, change)
