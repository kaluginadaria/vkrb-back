from django.contrib.postgres.search import SearchVectorField
from django.db import models


class SearchEntity(models.Model):
    entity_type = models.CharField(max_length=64)
    entity_id = models.IntegerField()
    body = models.TextField()
    search_vector = SearchVectorField()

    class Meta:
        unique_together = [
            ('entity_type', 'entity_id')
        ]
