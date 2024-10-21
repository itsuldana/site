from rest_framework import serializers

from webapp.models import LessonProgress


class ProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['lesson', 'status',]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'