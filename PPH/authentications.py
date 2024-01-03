from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Tentez de récupérer le token depuis un cookie
        jwt_token = request.COOKIES.get('access_token')

        if not jwt_token:
            return None

        # Utilisez le token pour authentifier l'utilisateur
        try:
            validated_token = self.get_validated_token(jwt_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except AuthenticationFailed as exc:
            return None