from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from film.views import *

router = DefaultRouter()
router.register("izohlar", IzohModelViewSet)
router.register("movies", KinoModelViewSet)
router.register("actor", AktyorModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelleApi.as_view()),
    path('aktyorlar/', AktyorlarAPi.as_view()),
    path('aktyor/<int:pk>/', AktyorAPi.as_view()),

    path('tariflar/', TariflarAPi.as_view()),
    path('tarif/<int:pk>/', TarifAPi.as_view()),

    path('kinolar/', KinolarAPi.as_view()),
    path('kino/<int:pk>/', KinoAPi.as_view()),

    path("", include(router.urls)),

    path('comment/', IzohListCreateAPIView.as_view()),
    path('token/', obtain_auth_token)
]
