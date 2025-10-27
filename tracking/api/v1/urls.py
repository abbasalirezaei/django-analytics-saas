from django.urls import path
from . import views

urlpatterns = [
    path('pageview/', views.PageViewAPI.as_view(), name='track-pageview'),
    path('event/', views.EventAPI.as_view(), name='track-event'),
    path('session/start/', views.SessionStartAPI.as_view(), name='session-start'),
    path('session/end/', views.SessionEndAPI.as_view(), name='session-end'),
    path('batch/', views.BatchTrackingAPI.as_view(), name='batch-tracking'),
]