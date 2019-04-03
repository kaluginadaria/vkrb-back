import io
import os

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_serializer.base_views import BaseView
from django_serializer.exceptions import ServerError
from django_serializer.mixins import CsrfExemptMixin, SerializerMixin
from django_serializer.permissions import PermissionsMixin

from vkrb.attachment.models import Attachment
from vkrb.attachment.serializers import AttachmentSerializer
from vkrb.core.image_utils import image_rotate
from vkrb.core.utils import calculate_image_hash


class UploadImageView(CsrfExemptMixin, PermissionsMixin, SerializerMixin,
                      BaseView):
    serializer = AttachmentSerializer
    image_max_size = (4000, 4000)

    def check_permission(self, user, permission):
        return None

    def get_serializer_kwargs(self, obj, **kwargs):
        kwargs = super().get_serializer_kwargs(obj, **kwargs)
        kwargs['multiple'] = True
        return kwargs

    def get_file_ext(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.strip('.')

    def generate_filename(self, file):
        file_hash = calculate_image_hash(file)
        ext = self.get_file_ext(file.name)
        return f'{file_hash}.{ext}'

    def check_request(self):
        user = self.request.user
        self.check_r_permission(user)

    def get_files(self, ct=None):
        number_of_files = 0

        for file in self.request.FILES.getlist('file'):
            if ct and file.content_type.lower() not in ct:
                continue
            yield file
            number_of_files += 1

        if number_of_files == 0:
            raise ServerError(ServerError.BAD_REQUEST)

    def save_file(self, file):
        file.name = self.generate_filename(file)

        attachment = Attachment(file=file)
        try:
            attachment.save()
        except:
            raise ServerError(ServerError.FILE_SAVE_ERROR)

        return attachment

    def save_image(self, file):
        filename = self.generate_filename(file)

        image = Image.open(file)
        image_format = image.format
        image = image_rotate(image)
        image.thumbnail(self.image_max_size, Image.ANTIALIAS)
        stream = io.BytesIO()
        image.save(stream, format=image_format)

        image_file = InMemoryUploadedFile(
            file=stream,
            field_name=None,
            name=filename,
            content_type=file.content_type,
            size=None,
            charset=None
        )

        return self.save_file(image_file)

    def get_meta(self, file):
        return {
            'content_type': file.content_type,
            'file': file.name,
        }

    def post(self, *args, **kwargs):
        self.check_request()

        attachments = []
        for image in self.get_files(settings.IMAGE_CONTENT_TYPES):
            attachment = self.save_image(image)
            attachments.append(attachment)

        return attachments
