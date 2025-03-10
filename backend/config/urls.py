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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("commons.urls")),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/user/", include("users.urls")),
    path("api/v1/organisms/", include("sinp_organisms.urls")),
    path("api/v1/cables/", include("cables.urls")),
    path("api/v1/geoareas/", include("geo_area.urls")),
    path("api/v1/sensitive-areas/", include("sensitive_area.urls")),
    path("api/v1/cables/", include("cables.urls")),
    path("api/v1/mortality/", include("mortality.urls")),
    path("api/v1/species/", include("species.urls")),
    path("api/v1/media/", include("media.urls")),
    path("api/v1/custom-content/", include("custom_content.urls")),
    path("api/v1/nomenclatures/", include("sinp_nomenclatures.urls")),
    path("api/v1/map-layers/", include("map_layers.urls")),
    path("api/admin/doc/", include("django.contrib.admindocs.urls")),
    path("api/admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEV:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version="v1",
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
