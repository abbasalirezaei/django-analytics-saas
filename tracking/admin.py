from django.contrib import admin
from .models import Website, Session, PageView, Event, DailyWebsiteStats, PageStats

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
	list_display = ['name', 'domain', 'organization', 'created_at', 'is_active']
	list_filter = ['organization', 'is_active']
	search_fields = ['name', 'domain']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
	list_display = ['session_id', 'website', 'started_at', 'device_type', 'country']
	list_filter = ['website', 'device_type', 'started_at']
	search_fields = ['session_id']

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
	list_display = ['website', 'session', 'page_url', 'timestamp']
	list_filter = ['website', 'timestamp']
	search_fields = ['page_url']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ['website', 'session', 'event_name', 'timestamp']
	list_filter = ['website', 'event_name', 'timestamp']
	search_fields = ['event_name']

@admin.register(DailyWebsiteStats)
class DailyWebsiteStatsAdmin(admin.ModelAdmin):
	list_display = ['website', 'date', 'pageviews', 'unique_visitors', 'sessions']
	list_filter = ['website', 'date']

@admin.register(PageStats)
class PageStatsAdmin(admin.ModelAdmin):
	list_display = ['website', 'page_url', 'date', 'views', 'unique_visitors']
	list_filter = ['website', 'date']
