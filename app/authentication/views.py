from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            user = serializer.user 

            response_data['user_id'] = user.id
            response_data['email'] = user.email 
            response_data['groups'] = [group.name for group in user.groups.all()]

            return Response(response_data, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer