from django.contrib.postgres.search import SearchVector
from django.db import transaction


class SearchModelMixin:
    def save(self, *args, **kwargs):
        from vkrb.search.models import SearchEntity
        from django.contrib.contenttypes.models import ContentType

        with transaction.atomic():
            super().save(*args, **kwargs)

            content_type = ContentType.objects.get_for_model(self)
            entity_type = f'{content_type.app_label}.{content_type.model}'
            entity_id = self.id
            body = self.get_text_for_search_vector()

            entity, created = SearchEntity.objects.get_or_create(
                entity_type=entity_type,
                entity_id=entity_id,
                defaults={'body': body}
            )
            if not created:
                entity.body = body
                entity.save()

            entity.search_vector = SearchVector('body')
            entity.save()

    def get_text_for_search_vector(self):
        raise NotImplementedError
