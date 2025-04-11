from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model, password_validation
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from Abstraction.builders.response_builder import ResponseBuilder
from user.serializers.auth_serializer import UserSerializer, LoginSerializer, PasswordResetSerializer

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        response_builder = ResponseBuilder()
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return response_builder.result_object(serializer.errors).fail().bad_request_404().message("Invalid input data").get_response()
        user = serializer.save()
        return response_builder.result_object(UserSerializer(user).data).success().ok_200().message("User created successfully!").get_response()


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response_builder = ResponseBuilder()
        if request.user.is_authenticated:
            return response_builder.result_object({"error": "You are already logged in"}).fail().bad_request_404().message("Already authenticated").get_response()
        
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response_builder.result_object(serializer.errors).fail().bad_request_404().message("Invalid input data").get_response()
        
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = get_user_model().objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return response_builder.result_object({"error": "Invalid credentials"}).fail().bad_request_404().message("Invalid credentials").get_response()
        
        # if not user.email_verified:
        #     return response_builder.result_object({"error": "Email not verified"}).fail().bad_request_404().message("Email verification required").get_response()

        if not user.is_active:
            return response_builder.result_object({"error": "User account is inactive"}).fail().bad_request_404().message("Account inactive").get_response()

        # Update last_login field
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token["role"] = user.role  # Add user role to the access token

        # Add user permissions to the access token
        permissions = user.user_permissions.all()
        permission_codenames = [perm.codename for perm in permissions]
        access_token["permissions"] = permission_codenames

        return response_builder.result_object({
            "refresh": str(refresh),
            "access": str(access_token),
        }).success().ok_200().message("Login successful").get_response()


class PasswordResetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @transaction.atomic
    def post(self, request):
        response_builder = ResponseBuilder()
        serializer = PasswordResetSerializer(data=request.data)
        
        if not serializer.is_valid():
            return response_builder.result_object(serializer.errors).fail().bad_request_404().message("Invalid input data").get_response()
        
        user = request.user
        new_password = serializer.validated_data['new_password']
        
        if user is None:
            return response_builder.result_object({}).fail().bad_request_404().message("Invalid email address").get_response()
        
        user.set_password(new_password)
        user.save()
        
        return response_builder.result_object({}).success().ok_200().message("Password has been reset successfully").get_response()