from django.urls import path, include
from . import views
urlpatterns = [

    path('v1/', include('tracking.api.v1.urls')),  # Version 1 API
]
