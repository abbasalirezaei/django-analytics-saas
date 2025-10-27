from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from accounts.api.v1.permissions import HasOrganizationAccess
from reporting.api.v1.serializers import (
    AnalyticsOverviewSerializer, TimeSeriesSerializer, TopPagesSerializer, 
    EventSummarySerializer, RealTimeStatsSerializer
)
from reporting.services.analytics_service import AnalyticsService
from reporting.utils.common import validate_date_range, format_analytics_data


class BaseAnalyticsView(APIView):
    """
    Base class for analytics views with common functionality
    """
    permission_classes = [IsAuthenticated, HasOrganizationAccess]
    
    def get_website_filters(self, website_id=None):
        """Get website filters for queries"""
        filters = {'website__organization': self.request.user.organization}
        if website_id:
            filters['website_id'] = website_id
        return filters
    
    def get_date_range(self, request):
        """Get date range from request parameters"""
        days = int(request.GET.get('days', 7))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date


class AnalyticsOverviewAPI(BaseAnalyticsView):
    def get(self, request):
        website_id = request.GET.get('website_id')
        days = int(request.GET.get('days', 7))

        data = AnalyticsService.get_analytics_overview(
            request.user.organization,
            website_id,
            days
        )

        serializer = AnalyticsOverviewSerializer(instance=data)
        return Response(serializer.data)


class TimeSeriesAPI(BaseAnalyticsView):
    def get(self, request):
        website_id = request.GET.get('website_id')
        days = int(request.GET.get('days', 7))
        
        data = AnalyticsService.get_time_series(
            request.user.organization, 
            website_id, 
            days
        )
        
        serializer = TimeSeriesSerializer(data, many=True)
        return Response(serializer.data)


class TopPagesAPI(BaseAnalyticsView):
    def get(self, request):
        website_id = request.GET.get('website_id')
        days = int(request.GET.get('days', 7))
        limit = int(request.GET.get('limit', 10))
        
        data = AnalyticsService.get_top_pages(
            request.user.organization, 
            website_id, 
            days, 
            limit
        )
        
        serializer = TopPagesSerializer(data, many=True)
        return Response(serializer.data)


class EventSummaryAPI(BaseAnalyticsView):
    def get(self, request):
        website_id = request.GET.get('website_id')
        days = int(request.GET.get('days', 7))
        
        data = AnalyticsService.get_event_summary(
            request.user.organization, 
            website_id, 
            days
        )
        
        serializer = EventSummarySerializer(data, many=True)
        return Response(serializer.data)



class RealTimeStatsAPI(BaseAnalyticsView):
    def get(self, request):
        website_id = request.GET.get('website_id')
        
        data = AnalyticsService.get_real_time_stats(
            request.user.organization, 
            website_id
        )
        
        serializer = RealTimeStatsSerializer(data)
        return Response(serializer.data)


class WebsiteListAPI(BaseAnalyticsView):
    def get(self, request):
        data = AnalyticsService.get_websites(request.user.organization)
        return Response(data)