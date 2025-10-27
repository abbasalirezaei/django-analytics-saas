from django.utils import timezone
from django.db.models import Count, Avg, Sum
from datetime import timedelta

from tracking.models import PageView, Event, Session, Website, DailyWebsiteStats, PageStats
from reporting.utils.cache_utils import AnalyticsCache

class AnalyticsService:
    """
    Service class for analytics and reporting operations.
    Provides methods to fetch overview stats, time series, top pages, event summaries, and real-time data.
    """

    @staticmethod
    def get_analytics_overview(organization, website_id=None, days=7):
        """
        Returns aggregated analytics overview for a given organization and optional website.
        Includes pageviews, visitors, sessions, events, session duration, and bounce rate.
        """
        cached_data = AnalyticsCache.get_overview_stats(organization.id, website_id, days)
        if cached_data:
            return cached_data

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days - 1)  # today is not aggregated yet

        base_filters = {'website__organization': organization}
        if website_id:
            base_filters['website_id'] = website_id

        # Aggregate historical stats from daily records
        stats = DailyWebsiteStats.objects.filter(
            **base_filters,
            date__range=[start_date, end_date]
        ).aggregate(
            total_pageviews=Sum('pageviews'),
            total_visitors=Sum('unique_visitors'),
            total_sessions=Sum('sessions'),
            avg_session_duration=Avg('avg_session_duration'),
        )

        # Count total events in the same period
        event_count = Event.objects.filter(
            **base_filters,
            timestamp__date__range=[start_date, end_date]
        ).count()

        # Fetch real-time stats (last 30 minutes + today)
        real_time_stats = AnalyticsService.get_real_time_stats(organization, website_id)

        # Combine historical and real-time data
        data = {
            'total_pageviews': (stats.get('total_pageviews') or 0) + real_time_stats.get('pageviews_today', 0),
            'total_visitors': (stats.get('total_visitors') or 0) + real_time_stats.get('active_visitors', 0),
            'total_sessions': (stats.get('total_sessions') or 0) + real_time_stats.get('sessions_today', 0),
            'total_events': event_count,
            'avg_session_duration': stats.get('avg_session_duration') or 0,
            'bounce_rate': 0,  # TODO: implement bounce rate calculation
            'period': f'{start_date} to {end_date}',
            'cached': False
        }

        # Cache the result for future use
        AnalyticsCache.set_overview_stats(organization.id, website_id, days, data)
        data['cached'] = True

        return data

    @staticmethod
    def get_time_series(organization, website_id=None, days=7):
        """
        Returns time series data for pageviews, visitors, and sessions over the last N days.
        Fills missing dates with zero values.
        """
        cached_data = AnalyticsCache.get_time_series(organization.id, website_id, days)
        if cached_data:
            return cached_data

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        base_filters = {'website__organization': organization}
        if website_id:
            base_filters['website_id'] = website_id

        # Fetch daily stats
        time_series_data = DailyWebsiteStats.objects.filter(
            **base_filters,
            date__range=[start_date, end_date]
        ).values('date', 'pageviews', 'unique_visitors', 'sessions').order_by('date')

        # Fill missing dates with zeroed entries
        date_map = {}
        current_date = start_date
        while current_date <= end_date:
            date_map[current_date] = {
                'date': current_date,
                'pageviews': 0,
                'visitors': 0,
                'sessions': 0
            }
            current_date += timedelta(days=1)

        for item in time_series_data:
            date_map[item['date']]['pageviews'] = item['pageviews']
            date_map[item['date']]['visitors'] = item['unique_visitors']
            date_map[item['date']]['sessions'] = item['sessions']

        result = list(date_map.values())

        # Cache the result
        AnalyticsCache.set_time_series(organization.id, website_id, days, result)

        return result

    @staticmethod
    def get_top_pages(organization, website_id=None, days=7, limit=10):
        """
        Returns top N pages based on views and average time on page.
        """
        cached_data = AnalyticsCache.get_top_pages(organization.id, website_id, days, limit)
        if cached_data:
            return cached_data

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        base_filters = {'website__organization': organization}
        if website_id:
            base_filters['website_id'] = website_id

        # Aggregate page stats
        top_pages = PageStats.objects.filter(
            **base_filters,
            date__range=[start_date, end_date]
        ).values('page_url').annotate(
            views=Sum('views'),
            avg_time_on_page=Avg('avg_time_on_page')
        ).order_by('-views')[:limit]

        top_pages_list = list(top_pages)

        # Cache the result
        AnalyticsCache.set_top_pages(organization.id, website_id, days, limit, top_pages_list)

        return top_pages_list

    @staticmethod
    def get_event_summary(organization, website_id=None, days=7):
        """
        Returns summary of events including count and unique users per event.
        """
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        base_filters = {'website__organization': organization}
        if website_id:
            base_filters['website_id'] = website_id

        date_filters = {'timestamp__date__range': [start_date, end_date]}

        # Aggregate event data
        event_summary = Event.objects.filter(
            **base_filters,
            **date_filters
        ).values('event_name').annotate(
            count=Count('id'),
            unique_users=Count('session_id', distinct=True)
        ).order_by('-count')

        return list(event_summary)

    @staticmethod
    def get_real_time_stats(organization, website_id=None):
        """
        Returns real-time stats including active visitors, today's pageviews, and popular pages.
        """
        base_filters = {'website__organization': organization}
        if website_id:
            base_filters['website_id'] = website_id

        # Active sessions in last 30 minutes
        active_visitors = Session.objects.filter(
            **base_filters,
            started_at__gte=timezone.now() - timedelta(minutes=30)
        ).count()

        # Pageviews since start of today
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        pageviews_today = PageView.objects.filter(
            **base_filters,
            timestamp__gte=today_start
        ).count()

        # Top 5 popular pages today
        popular_pages = PageView.objects.filter(
            **base_filters,
            timestamp__gte=today_start
        ).values('page_url', 'page_title').annotate(
            views=Count('id')
        ).order_by('-views')[:5]

        return {
            'active_visitors': active_visitors,
            'pageviews_today': pageviews_today,
            'sessions_today': Session.objects.filter(
                **base_filters,
                started_at__gte=today_start
            ).count(),
            'popular_pages': list(popular_pages)
        }

    @staticmethod
    def get_websites(organization):
        """
        Returns list of active websites for the given organization.
        """
        websites = Website.objects.filter(
            organization=organization,
            is_active=True
        )

        return [{
            'id': website.id,
            'name': website.name,
            'domain': website.domain,
            'created_at': website.created_at
        } for website in websites]