import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    auth_header_prefix = "Bearer".lower()

    def authenticate(self, request):
        """
        This method is called everytime you try accessing an endpoint, incase you what
        authentication to fail it will return None, i.e when no authentication credentials
        are provided. Incase of an error, we raise authentication failed error
        """

        request.user = None
        # we need the auth_header, which should be a list containing two
        # elements: 1) the name of the authentication header ('Bearer' in our
        # case) and 2) the JWT token.
        auth_header = authentication.get_authorization_header(request).split()
        # Bearer kjdksjdskdjskjskdskjdsdkjsdksdksjdkjsdskdsdskjdsjkdjsd
        # [Bearer, dsddsdlskdlks]
        if not auth_header:
            # if we get no authentication header, we do not attempt to
            # authenticate
            return None

        if len(auth_header) == 1:
            # We expect the length to be 2, so this is an invalid header. Do
            # not attempt to authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The length must be 2. Do not attempt
            # to authenticate
            return None

        # We have to decode both the prefix and token because they are in bytes,
        # and the JWT library we use can't handly bytes.
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != self.auth_header_prefix:
            # The auth header prefix should only be 'Bearer'. If otherwise,
            # don't attempt to authenticate
            return None

        # We can now attempt to authenticate after performing the above checks.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        We will try to authenticate the token. If authentication is successful
        we return (user, token), otherwise we return an `AuthenticationFailed`
        error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        except jwt.ExpiredSignatureError:
            msg = "Your token has expired, please log in again."
            raise exceptions.AuthenticationFailed(msg)

        except Exception as e:
            msg = str(e)
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            msg = "User not found"
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "Forbidden! This user has been deactivated."
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
