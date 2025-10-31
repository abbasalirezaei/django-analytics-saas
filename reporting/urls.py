from django.urls import include, path

urlpatterns = [
    path("v1/", include("reporting.api.v1.urls")),
]
