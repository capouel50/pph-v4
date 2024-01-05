from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import admin
from .views import (
    home, CurrentUserView, ContactView, SupplierViewSet, UserFunctionListCreateView, CustomUserListCreateView,
    CustomUserRetrieveUpdateDestroyView, TypeMatiereViewSet, UniteMesureViewSet, FormeViewSet,
    CompositionViewSet, FormuleViewSet, MatierePremiereViewSet, CatalogueViewSet, ListeViewSet,
    VoieViewSet, TypePrepViewSet, ParametresPrepViewSet, ParametresFormulesViewSet, CompositionFilterView
)
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'types-matiere', TypeMatiereViewSet)
router.register(r'unites-mesure', UniteMesureViewSet)
router.register(r'formes', FormeViewSet)
router.register(r'matieres-premieres', MatierePremiereViewSet)
router.register(r'nouvelle-formule', FormuleViewSet)
router.register(r'composition', CompositionViewSet, basename='composition')
router.register(r'catalogue', CatalogueViewSet)
router.register(r'voie', VoieViewSet)
router.register(r'liste', ListeViewSet)
router.register(r'type-prep', TypePrepViewSet)
router.register(r'parametres-prep', ParametresPrepViewSet)
router.register(r'parametres-formules', ParametresFormulesViewSet)

urlpatterns = [
    path('', admin.site.urls),
    path('composition/filter/<int:num_formule>/', CompositionFilterView.as_view(), name='composition-filter'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
    path('contact/', ContactView.as_view(), name='contact-create'),
    path('user/update/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-update'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/', CustomUserListCreateView.as_view(), name='custom-user-list'),
    path('user-functions/', UserFunctionListCreateView.as_view(), name='user-function-list'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


