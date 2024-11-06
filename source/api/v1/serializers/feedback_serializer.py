from rest_framework import serializers

from webapp.models import Feedback

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

