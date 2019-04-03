from adminsortable2.admin import CustomInlineFormSet
from django.core.exceptions import ValidationError


class NewsItemAttachmentAdminForm(CustomInlineFormSet):

    def clean(self):
        super().clean()
        photos = self.cleaned_data
        main_photos = [photo for photo in photos if photo['main'] is True]
        if len(main_photos) != 1:
            raise ValidationError('Выберете одно главное фото')
