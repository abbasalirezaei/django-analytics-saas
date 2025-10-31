from rest_framework import serializers

from tracking.models import DailyWebsiteStats, Event, PageStats, PageView, Session


class AnalyticsOverviewSerializer(serializers.Serializer):
    total_pageviews = serializers.IntegerField()
    total_visitors = serializers.IntegerField()
    total_sessions = serializers.IntegerField()
    total_events = serializers.IntegerField()
    avg_session_duration = serializers.FloatField()
    bounce_rate = serializers.FloatField()
    period = serializers.CharField()
    cached = serializers.BooleanField(required=False)


class TimeSeriesSerializer(serializers.Serializer):
    date = serializers.DateField()
    pageviews = serializers.IntegerField()
    visitors = serializers.IntegerField()
    sessions = serializers.IntegerField()


class PageStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageStats
        fields = [
            "page_url",
            "date",
            "views",
            "unique_visitors",
            "avg_time_on_page",
            "exit_rate",
        ]


class TopPagesSerializer(serializers.Serializer):
    page_url = serializers.CharField()
    views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    avg_time_on_page = serializers.FloatField()


class EventSummarySerializer(serializers.Serializer):
    event_name = serializers.CharField()
    count = serializers.IntegerField()
    unique_users = serializers.IntegerField()


class RealTimeStatsSerializer(serializers.Serializer):
    active_visitors = serializers.IntegerField()
    pageviews_today = serializers.IntegerField()
    popular_pages = serializers.ListField(child=serializers.DictField())
