from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterCustomUserSerializers, LoginSerializers, ProfileSerializers, ChangePasswordSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        ser_data = RegisterCustomUserSerializers(data= request.data)
        if ser_data.is_valid():
            user = ser_data.create(ser_data.validated_data)
            jwt = RefreshToken.for_user(user= user)
            return Response(data= {
                'refresh_token': str(jwt),
                'access_token': str(jwt.access_token),
                'Message': 'Register Successful.',
            }, status=status.HTTP_201_CREATED)

        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        ser_data = LoginSerializers(data= request.data)

        if ser_data.is_valid():
            email = ser_data.validated_data["email"]
            password = ser_data.validated_data["password"]
            user = CustomUser.objects.filter(email= email).first()

            if not user or not user.check_password(password):
                return Response(data= {
                    'Message': 'Email/Password is wrong ... ',
                }, status=status.HTTP_400_BAD_REQUEST)

            jwt = RefreshToken.for_user(user)
            return Response(data={
                'refresh_token': str(jwt),
                'access_token': str(jwt.access_token),
                'Message': 'Login Successful.',
            }, status=status.HTTP_200_OK)

        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            token = RefreshToken(refresh)
            token.blacklist()

            return Response({'Message': 'Logout Successful.', 'login_url': '/login/',}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'Message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]


    def get(self, request):
        user_profile = CustomUser.objects.get(email= request.user.email)
        ser_data = ProfileSerializers(instance= user_profile)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = CustomUser.objects.get(email= request.user.email)
        ser_data = ProfileSerializers(data= request.data, instance= user, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return redirect('profile-page')
        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = CustomUser.objects.get(email= request.user.email)
        ser_data = ChangePasswordSerializers(data= request.data)

        if ser_data.is_valid():
            old_password = ser_data.validated_data["old_password"]
            new_password = ser_data.validated_data["new_password"]
            if not user.check_password(old_password):
                return Response(data= {
                    'Message': 'Old Password is not correct '
                }, status= status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            jwt = request.data.get('refresh')
            if jwt:
                token = RefreshToken(jwt)
                token.blacklist()

            return Response(data= {
                'Message': 'Password Change Success. Please Login again .',
                'login_url': '/login/',
            }, status=status.HTTP_200_OK)

        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)