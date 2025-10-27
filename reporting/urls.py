from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('reporting.api.v1.urls')),
]
