from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import PurchaseCreateSerializer


@extend_schema(tags=['purchase'])
class PurchaseCreateApiView(APIView):
    @extend_schema(
        request=PurchaseCreateSerializer,
        responses=PurchaseCreateSerializer
    )
    def post(self, request):
        data = request.data
        user = request.user

        serializer = PurchaseCreateSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
