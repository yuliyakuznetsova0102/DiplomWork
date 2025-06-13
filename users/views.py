from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    UserRegistrationSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "If this email exists, a password reset link has been sent."},
                status=status.HTTP_200_OK
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        print(f"Generated UID: {uid}, Token: {token}")

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        print(f"Reset URL: {reset_url}")

        try:
            send_mail(
                subject="Password Reset Request",
                message=f"Please go to the following link to reset your password:\n\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(
                {"message": "Password reset link has been sent to your email."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return Response(
                {"message": "Failed to send reset link. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, serializer.validated_data['token']):
                return Response(
                    {"message": "Invalid or expired reset link."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(f"Error during password reset: {str(e)}")
            return Response(
                {"message": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )
