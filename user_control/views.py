from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from .serializers import CreateUSerSerializer, CustomUser, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from inventory_api.utils import get_access_token
from inventory_api.custom_methods import IsAuthenticatedCustom


class CreateUserView(ModelViewSet):
    http_method_names = ['post']
    queryset = CustomUser.objects.all()
    serializer_class = CreateUSerSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)

        CustomUser.objects.create(**valid_request.validated_data)

        return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(ModelViewSet):
    http_method_names = ['post']
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer()

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        new_user = valid_request.validated_data['is_new_user']
        if new_user:
            user = CustomUser.objects.filter(
                email = valid_request.validated_data['email']
                )
            if user:
                user = user[0]
                if not user.password:
                    return Response({'user_id': user.id})
            else:
                return Exception("User has password already")
        else:
            raise Exception("User with email not found")

        user = authenticate(
            username=valid_request.validated_data['email'],
            password=valid_request.validated_data.get("password", None)
        )

        if not user:
            return Response({'error': "invalid email or Password"}, status=status.HTTP_400_BAD_REQUEST)

        access = get_access_token({"user_id": user.id}, 1)

        user.last_login = datetime.now()

        return Response({"access": access})

