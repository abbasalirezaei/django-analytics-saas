from django.urls import path
from . import views

urlpatterns = [
    # Analytics Overview
    path('overview/', views.AnalyticsOverviewAPI.as_view(), name='analytics-overview'),
    
    # Time Series Data
    path('timeseries/', views.TimeSeriesAPI.as_view(), name='analytics-timeseries'),
    
    # Top Pages
    path('top-pages/', views.TopPagesAPI.as_view(), name='analytics-top-pages'),
    
    # Event Summary
    path('events/', views.EventSummaryAPI.as_view(), name='analytics-events'),
    
    # Real-time Stats
    path('realtime/', views.RealTimeStatsAPI.as_view(), name='analytics-realtime'),
    
    # Websites
    path('websites/', views.WebsiteListAPI.as_view(), name='analytics-websites'),
]
