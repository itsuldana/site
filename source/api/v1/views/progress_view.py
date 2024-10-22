from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize

from api.v1.serializers import ProgressCreateSerializer
from api.v1.serializers.progress_serializer import ProgressSerializer
from webapp.models import LessonProgress


@extend_schema(tags=['lesson_progress'])
class ProgressApiView(APIView):
    @extend_schema(
        request=ProgressCreateSerializer,
        responses=ProgressCreateSerializer,
    )
    def post(self, request):
        data = request.data
        user = request.user
        lesson_id = request.data.get('lesson')

        if LessonProgress.objects.filter(lesson_id=lesson_id, user=user).exists():
            return Response(
                {"message": "Progress already exists, no action taken."},
                status=status.HTTP_200_OK
            )

        serializer = ProgressCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['lesson_progress'])
class ProgressUpdateApiView(APIView):
    @extend_schema(
        request=ProgressSerializer,
        responses=ProgressSerializer
    )
    def put(self, request, lesson_id):
        user = request.user
        try:
            progress = LessonProgress.objects.get(lesson_id=lesson_id, user=user)
        except LessonProgress.DoesNotExist:
            return Response({'error': 'Lesson progress not found'}, status=status.HTTP_404_NOT_FOUND)

        progress.status = 'done'
        progress.finished_at = timezone.now()
        progress.save()

        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)
