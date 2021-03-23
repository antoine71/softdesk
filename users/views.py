from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import status
from rest_framework.response import Response

from .serializers import MyTokenObtainSerializer, UserSerializer


class CreateUserView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainView(TokenViewBase):
    serializer_class = MyTokenObtainSerializer
