from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Avg, F
from django.db.models.functions import Extract
from datetime import timedelta, date
import logging

from .models import Website, Session, PageView, Event, DailyWebsiteStats, PageStats
from .cache import AnalyticsCache

logger = logging.getLogger(__name__)

@shared_task
def aggregate_daily_stats():
    """
    Aggregate daily statistics for all websites
    Runs daily to precompute metrics
    """
    try:
        yesterday = timezone.now().date() - timedelta(days=1)
        websites = Website.objects.filter(is_active=True)
        stats_created = 0
        for website in websites:
            # Calculate daily metrics
            daily_filters = {
                'website': website,
                'timestamp__date': yesterday
            }
            pageview_data = PageView.objects.filter(
                **daily_filters
            ).aggregate(
                total_pageviews=Count('id'),
                unique_visitors=Count('session_id', distinct=True)
            )
            session_data = Session.objects.filter(
                website=website,
                started_at__date=yesterday
            ).aggregate(
                total_sessions=Count('id')
            )
            event_count = Event.objects.filter(
                **daily_filters
            ).count()
            session_duration = Session.objects.filter(
                website=website,
                started_at__date=yesterday,
                ended_at__isnull=False
            ).annotate(
                duration=Extract(F('ended_at') - F('started_at'), 'seconds')
            ).aggregate(
                avg_duration=Avg('duration')
            )
            bounce_sessions = Session.objects.filter(
                website=website,
                started_at__date=yesterday
            ).annotate(
                pageview_count=Count('pageviews')
            ).filter(pageview_count=1).count()
            total_sessions = session_data['total_sessions'] or 0
            bounce_rate = (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0
            # Aggregate DailyWebsiteStats
            DailyWebsiteStats.objects.update_or_create(
                website=website,
                date=yesterday,
                defaults={
                    'pageviews': pageview_data['total_pageviews'],
                    'unique_visitors': pageview_data['unique_visitors'],
                    'sessions': session_data['total_sessions'],
                    'avg_session_duration': session_duration['avg_duration'] or 0,
                    'bounce_rate': bounce_rate,
                }
            )
            # Aggregate PageStats
            page_urls = PageView.objects.filter(
                website=website,
                timestamp__date=yesterday
            ).values_list('page_url', flat=True).distinct()
            for page_url in page_urls:
                pageviews_for_url = PageView.objects.filter(
                    website=website,
                    timestamp__date=yesterday,
                    page_url=page_url
                ).count()
                # Placeholder for avg_time_on_page calculation
                avg_time_on_page = 0

                PageStats.objects.update_or_create(
                    website=website,
                    date=yesterday,
                    page_url=page_url,
                    defaults={
                        'views': pageviews_for_url,
                        'avg_time_on_page': avg_time_on_page,
                    }
                )
            # Invalidate cache for this website
            AnalyticsCache.invalidate_website_cache(
                website.id, website.organization.id
            )
            stats_created += 1
        logger.info(f"Aggregated daily stats for {stats_created} websites")
        return f"Created {stats_created} daily stats records"
    except Exception as e:
        logger.error(f"Error in aggregate_daily_stats: {str(e)}")
        raise

@shared_task
def cleanup_old_sessions():
    """
    Clean up old sessions and associated data
    Keep data for 90 days for compliance and analysis
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        old_sessions = Session.objects.filter(started_at__lt=cutoff_date)
        session_count = old_sessions.count()
        batch_size = 1000
        deleted_count = 0
        while old_sessions.exists():
            batch_ids = old_sessions.values_list('id', flat=True)[:batch_size]
            PageView.objects.filter(session_id__in=batch_ids).delete()
            Event.objects.filter(session_id__in=batch_ids).delete()
            Session.objects.filter(id__in=batch_ids).delete()
            deleted_count += len(batch_ids)
            logger.info(f"Cleaned up {deleted_count}/{session_count} old sessions")
        logger.info(f"Session cleanup completed: {deleted_count} sessions deleted")
        return f"Cleaned up {deleted_count} old sessions"
    except Exception as e:
        logger.error(f"Error in cleanup_old_sessions: {str(e)}")
        raise

@shared_task
def update_realtime_cache():
    """
    Update real-time statistics cache
    Runs frequently to keep real-time data fresh
    """
    try:
        from django.core.cache import cache
        websites = Website.objects.filter(is_active=True)
        for website in websites:
            cache_key = f"realtime:website:{website.id}"
            active_visitors = Session.objects.filter(
                website=website,
                started_at__gte=timezone.now() - timedelta(minutes=30)
            ).count()
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            pageviews_today = PageView.objects.filter(
                website=website,
                timestamp__gte=today_start
            ).count()
            popular_pages = PageView.objects.filter(
                website=website,
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).values('page_url', 'page_title').annotate(
                views=Count('id')
            ).order_by('-views')[:5]
            realtime_data = {
                'active_visitors': active_visitors,
                'pageviews_today': pageviews_today,
                'popular_pages': list(popular_pages),
                'updated_at': timezone.now().isoformat()
            }
            cache.set(cache_key, realtime_data, timeout=120)  # 2 minutes
        logger.info("Real-time cache updated")
        return "Real-time cache updated"
    except Exception as e:
        logger.error(f"Error in update_realtime_cache: {str(e)}")
        raise
