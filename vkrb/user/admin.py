from django.contrib import admin
from django.utils.safestring import mark_safe

from vkrb.client.push import NewUserChangedItemPush
from vkrb.core.utils import build_url
from vkrb.user.forms import UserAdminChangedForm
from vkrb.user.models import UserChanged


@admin.register(UserChanged)
class CustomUserChangedAdmin(admin.ModelAdmin):
    list_display = ['user', "status"]
    readonly_fields = ('user',
                       'get_old_photo', 'image_tag',
                       'get_old_age', 'age',
                       'get_old_experience', 'experience',
                       'get_old_occupations', 'occupations',
                       'get_old_interests', 'interests',
                       'get_old_phone', 'phone',
                       'get_old_first_name', 'first_name',
                       'get_old_last_name', 'last_name',
                       'get_old_company', 'company',
                       'get_old_location', 'location'
                       )

    ordering = ('created_date',)
    form = UserAdminChangedForm
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')

    def get_old_photo(self, obj):
        if obj.user.photo:
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(obj.user.photo.file.url))
        else:
            return '-'

    get_old_photo.short_description = 'Старое фото'

    def image_tag(self, obj):
        if obj.photo:
            return mark_safe(
                '<div style="background-position: center;'
                ' background-repeat: no-repeat;'
                ' background-size: cover;'
                ' background-image: url(%s);'
                ' height: 150px;'
                ' width: 150px;" />' % build_url(obj.photo.file.url))
        else:
            return '-'

    image_tag.short_description = 'Новое фото'


    def get_old_age(self, obj):
        return obj.user.age if obj.user.age else '-'

    get_old_age.short_description = 'Старый возраст'

    def get_old_experience(self, obj):
        return obj.user.experience if obj.user.experience else '-'

    get_old_experience.short_description = 'Старый стаж работы'

    def get_old_occupations(self, obj):
        return obj.user.occupations if obj.user.occupations else '-'

    get_old_occupations.short_description = 'Старый род деятельности'

    def get_old_interests(self, obj):
        return obj.user.interests if obj.user.interests else '-'

    get_old_interests.short_description = 'Старые интересные темы'

    def get_old_phone(self, obj):
        return obj.user.phone

    get_old_phone.short_description = 'Старый телефон'

    def get_old_first_name(self, obj):
        return obj.user.first_name

    get_old_first_name.short_description = 'Старое имя'

    def get_old_last_name(self, obj):
        return obj.user.last_name

    get_old_last_name.short_description = 'Старая фамилия'

    def get_old_company(self, obj):
        return obj.user.company

    get_old_company.short_description = 'Старая компания'

    def get_old_location(self, obj):
        return obj.user.location

    get_old_location.short_description = 'Старое местонахождение'
