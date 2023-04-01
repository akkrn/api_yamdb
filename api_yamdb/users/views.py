from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin, IsUser, IsModerator
from .serializers import UserSerializer, TestUserSerializer, \
    ConfirmationCodeSerializer, UserMeSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'head', 'post', 'delete']


class UserMeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMeSerializer
    http_method_names = ['get', 'post', 'patch', 'head']


    def get_queryset(self):
        queryset = User.objects.filter(user=self.request.user)
        return queryset


#
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def signup(request):
#     email = request.data.get("email")
#     username = request.data.get("username")
#     if not email or not username:
#         return Response(
#             {"error": "Email and username are required"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     serializer = UserSerializer(data=request.data)
#     user = User.objects.get(username=username, email=email)
#     if serializer.is_valid() or user.exists():
#         confirmation_code = default_token_generator.make_token(user)
#         send_mail(
#             "Confirm your registration",
#             f"Your confirmation code is: {confirmation_code}",
#             'admin@example.com',
#             [email],
#             fail_silently=False,
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def token(request):
#     username = request.data.get("username")
#     confirmation_code = request.data.get("confirmation_code")
#     if not username or not confirmation_code:
#         return Response(
#             {"error": "Username and confirmation code are required"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     user = User.objects.get(username=username)
#     if not default_token_generator.check_token(user, confirmation_code):
#         return Response(
#             {"error": "Confirmation code is invalid"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     token = RefreshToken.for_user(user).access_token
#     response_data = {
#         "access": str(token),
#     }
#     return Response(response_data, status=status.HTTP_200_OK)

class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TestUserSerializer(data=request.data)
        email = request.data.get("email")
        username = request.data.get("username")

        if serializer.is_valid():
            user, created = User.objects.get_or_create(username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                "Confirm your registration",
                f"Your confirmation code is: {confirmation_code}",
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'email': email, 'username': username},
                            status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    serializer_class = ConfirmationCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        confirmation_code = request.data.get("confirmation_code")
        username = request.data.get("username")
        if not username or not confirmation_code:
            return Response(
                        {"error": "Username and confirmation code are required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        if not User.objects.get(username=username).exists():
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data[
                'username'])
            if user and default_token_generator.check_token(user,
                                                            serializer.validated_data[
                                                                'confirmation_code']):
                token = RefreshToken.for_user(user)
                return Response({'token': str(token.access_token)},
                                status=status.HTTP_200_OK)
            return Response({'error': 'Invalid confirmation code'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
