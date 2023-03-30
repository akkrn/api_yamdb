from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import RegistrationSerializer


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create an access token for the newly registered user
        token = AccessToken.for_user(user)

        # Send an email to the user with the access token
        # (You will need to implement this yourself)
        send_registration_email(user.email, str(token))

        return Response({'message': 'User registered successfully'})