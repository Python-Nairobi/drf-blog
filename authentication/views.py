from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer


# ListCreateAPIView, RetrieveUpdateDestroyAPIView
# List and create
# Get One(get), Destroy(Delete), Update(Update)


# Princples:
# HTTP Methods DELETE, POST, PATCH, PUT, GET
# Status Codes: 200 OK, 400 BAD REQUEST, 201 CREATED, 403 401 //Authentication and Authorization


class RegistrationAPIView(GenericAPIView):
    """Register new users."""

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # send email here

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """api view for user login"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data
        repsonse = {
            "data": {"user": dict(user), "message": "You have successfuly logged in"}
        }
        return Response(repsonse, status=status.HTTP_200_OK)
