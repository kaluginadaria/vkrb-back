from django_serializer.serializer.base import ModelSerializer

from vkrb.feedback.models import CategoryFeedback


class CategoryFeedbackSerializer(ModelSerializer):
    class Meta:
        model = CategoryFeedback



