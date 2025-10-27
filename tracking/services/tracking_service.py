from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from tracking.models import Website, Session, PageView, Event
from tracking.utils.cache_utils import get_or_set_cache


class TrackingService:
    """
    Service class for tracking-related operations
    """

    @staticmethod
    def record_pageview(domain, session_id, data):
        """
        Record a page view event with caching
        """
        cache_key = f"pageview:{domain}:{session_id}"

        def fetch_data():
            try:
                website = Website.objects.get(domain=domain, is_active=True)
                session, _ = Session.objects.get_or_create(
                    website=website,
                    session_id=session_id
                )
                PageView.objects.create(
                    website=website,
                    session=session,
                    **data,
                    timestamp=timezone.now()
                )
                return {'status': 'ok'}
            except Website.DoesNotExist:
                return {'error': 'Website not found'}
            except Exception as e:
                return {'error': str(e)}

        return get_or_set_cache(cache_key, fetch_data, timeout=300)

    @staticmethod
    def record_event(domain, session_id, data):
        """
        Record a custom event with caching
        """
        cache_key = f"event:{domain}:{session_id}"

        def fetch_data():
            try:
                website = Website.objects.get(domain=domain, is_active=True)
                session, _ = Session.objects.get_or_create(
                    website=website,
                    session_id=session_id
                )
                Event.objects.create(
                    website=website,
                    session=session,
                    **data,
                    timestamp=timezone.now()
                )
                return {'status': 'ok'}
            except Website.DoesNotExist:
                return {'error': 'Website not found'}
            except Exception as e:
                return {'error': str(e)}

        return get_or_set_cache(cache_key, fetch_data, timeout=300)

    @staticmethod
    def start_session(domain, data):
        """
        Start a new session
        """
        try:
            website = Website.objects.get(domain=domain, is_active=True)
            session = Session.objects.create(
                website=website,
                **data,
                started_at=timezone.now()
            )
            return session, {'status': 'ok', 'session_id': session.session_id}
        except Website.DoesNotExist:
            return None, {'error': 'Website not found'}
        except Exception as e:
            return None, {'error': str(e)}

    @staticmethod
    def end_session(domain, session_id):
        """
        End an existing session
        """
        try:
            website = Website.objects.get(domain=domain, is_active=True)
            session = Session.objects.get(website=website, session_id=session_id)
            session.ended_at = timezone.now()
            session.save()
            return {'status': 'ok'}
        except (Website.DoesNotExist, Session.DoesNotExist):
            return {'error': 'Session or website not found'}
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def batch_track_events(events_data):
        """
        Process multiple tracking events in batch
        """
        errors = []
        successful_count = 0

        with transaction.atomic():
            for item in events_data:
                try:
                    domain = item.get('domain')
                    session_id = item.get('session_id')
                    event_type = item.get('type', 'pageview')

                    if event_type == 'pageview':
                        result = TrackingService.record_pageview(domain, session_id, item)
                    elif event_type == 'event':
                        result = TrackingService.record_event(domain, session_id, item)
                    else:
                        errors.append({'error': 'Invalid event type', 'item': item})
                        continue

                    if 'error' in result:
                        errors.append({'error': result['error'], 'item': item})
                    else:
                        successful_count += 1

                except Exception as e:
                    errors.append({'error': str(e), 'item': item})

        if errors:
            return {
                'status': 'partial',
                'successful_count': successful_count,
                'errors': errors
            }

        return {
            'status': 'ok',
            'successful_count': successful_count
        }