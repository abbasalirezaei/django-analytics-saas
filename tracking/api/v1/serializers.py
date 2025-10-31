from rest_framework import serializers

from ...models import Event, PageView, Session, Website


class PageViewSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)
    session_id = serializers.CharField(max_length=100)
    user_agent = serializers.CharField(write_only=True, required=False)
    ip_address = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PageView
        fields = [
            "domain",
            "session_id",
            "page_url",
            "page_title",
            "referrer",
            "load_time",
            "user_agent",
            "ip_address",
        ]
        read_only_fields = ["website", "session"]


class EventSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)
    session_id = serializers.CharField(max_length=100)
    user_agent = serializers.CharField(write_only=True, required=False)
    ip_address = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = [
            "domain",
            "session_id",
            "event_name",
            "event_data",
            "page_url",
            "user_agent",
            "ip_address",
        ]
        read_only_fields = ["website", "session"]


class SessionStartSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)

    class Meta:
        model = Session
        fields = [
            "domain",
            "session_id",
            "user_agent",
            "ip_address",
            "country",
            "browser",
            "device_type",
        ]
        read_only_fields = ["website"]


class SessionEndSerializer(serializers.Serializer):
    domain = serializers.CharField()
    session_id = serializers.CharField(max_length=100)
