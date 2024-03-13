from auth_account.models import Account
from auth_account.serializers import AccountSerializer
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class AccountViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()

    def list(self, request):

        queryset = self.queryset

        user_id = request.query_params.get("user_id")

        # queryset = queryset.filter(id=user_id)

        queryset = Account.objects.get(id=user_id)

        serializer = AccountSerializer(queryset)
        return Response(serializer.data)


class JWTSetCookieMixin:

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                response.data["refresh"],
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )
        if response.data.get("access"):
            response.set_cookie(
                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data["access"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )

        del response.data["access"]
        return super().finalize_response(request, response, *args, **kwargs)


class JWTCookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    pass
