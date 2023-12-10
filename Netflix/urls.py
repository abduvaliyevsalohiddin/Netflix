from django.contrib import admin
from django.urls import path

from film.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelleApi.as_view()),
    path('aktyorlar/', AktyorlarAPi.as_view()),
    path('aktyor/<int:pk>/', AktyorAPi.as_view()),

    path('tariflar/', TariflarAPi.as_view()),
    path('tarif/<int:pk>/', TarifAPi.as_view()),

]
