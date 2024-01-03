from django.contrib import admin
from django.urls import path, include
from PPH import views
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from PPH.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('PPH/', include('PPH.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('PPH/validate-account/<slug:uidb64>/<slug:token>/', views.ValidateAccountView.as_view(), name='validate_account'),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('accounts/register/', views.CustomRegisterView.as_view(), name='account_signup'),
    path('logout/', views.logout, name='logout'),
    path('login/', LoginView.as_view(), name='rest_login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
