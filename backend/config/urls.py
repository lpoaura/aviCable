"""Overhead Cables And Birdlife backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/cables/", include("cables.urls")),
    path("api/geo/", include("geo_area.urls")),
    path("api/sensitive/", include("sensitive_area.urls")),
    path("api/mortality/", include("mortality.urls")),
    path("media/", include("media.urls")),
    path("api/v1/", include("sinp_nomenclatures.urls")),
    path("admin/", admin.site.urls),
]