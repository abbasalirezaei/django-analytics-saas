from django.urls import include, path

app_name = "tracking"
urlpatterns = [
    path("v1/", include("tracking.api.v1.urls",
         namespace="api_v1")),  # Version 1 API
]
