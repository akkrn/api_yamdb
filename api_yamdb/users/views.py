from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from ..api_yamdb import settings


# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
#
# serializer = CatSerializer(data=request.data)
# if serializer.is_valid():
#     # Если полученные данные валидны —
#     # сохраняем данные в базу через save().
#     serializer.save()
#     # Возвращаем JSON со всеми данными нового объекта
#     # и статус-код 201
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
# # Если данные не прошли валидацию —
# # возвращаем информацию об ошибках и соответствующий статус-код:
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signup(request):
    email = request.data.get("email")
    username = request.data.get("username")
    if not email or not username:
        return Response(
            {"error": "Email and username are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, email=email)

    confirmation_code = RefreshToken.for_user(user).access_token

    send_mail(
        "Confirm your registration",
        f"Your confirmation code is: {confirmation_code}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response(
        {"success": "Confirmation code sent to your email"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def token(request):
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code")
    if not username or not confirmation_code:
        return Response(
            {"error": "Username and confirmation code are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(username=username)
        token = RefreshToken(confirmation_code)
        token_payload = token.payload
        if token_payload.get("user_id") != str(user.id):
            raise ValueError("Invalid token")
    except (User.DoesNotExist, ValueError) as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token.access_token
    response_data = {
        "access": str(access_token),
        "refresh": str(token),
    }
    return Response(response_data, status=status.HTTP_200_OK)
