from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import FeedbackCreateSerializer
from webapp.models import Feedback


@extend_schema(tags=['feedback'])
class FeedbackApiView(APIView):
    @extend_schema(
        request=FeedbackCreateSerializer,
        responses=FeedbackCreateSerializer,
    )
    def post(self, request):
        data = request.data
        user = request.user
        lesson_id = request.data.get('lesson')
        feedback_type = data.get('feedback_type')

        feedback, created = Feedback.objects.get_or_create(
            lesson_id=lesson_id,
            user=user,
            defaults={'feedback_type': feedback_type}
        )

        if not created:
            feedback.feedback_type = feedback_type
            feedback.save()
            return Response(
                {"message": "Progress already exists, no action taken."},
                status=status.HTTP_200_OK
            )

        serializer = FeedbackCreateSerializer(data=data)

        return Response(serializer.data, status=status.HTTP_200_OK)

