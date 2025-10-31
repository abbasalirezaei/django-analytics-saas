from django.urls import include, path

urlpatterns = [
    path("v1/", include("tracking.api.v1.urls")),  # Version 1 API
]
