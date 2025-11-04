from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ...services.tracking_service import TrackingService
from ...utils.common import detect_browser, detect_device_type, get_client_info
from .serializers import (
    EventSerializer,
    PageViewSerializer,
    SessionEndSerializer,
    SessionStartSerializer,
)


class SessionStartAPI(APIView):
    """
    Register a new user session when tracking begins
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SessionStartSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data.pop("domain")

            # Add client info(user_agent, ip_address, country) if not provided
            client_info = get_client_info(request)
            if "user_agent" not in serializer.validated_data:
                serializer.validated_data["user_agent"] = client_info["user_agent"]
            if "ip_address" not in serializer.validated_data:
                serializer.validated_data["ip_address"] = client_info["ip_address"]
            if "country" not in serializer.validated_data:
                serializer.validated_data["country"] = client_info["country"]

            # Detect device type and browser
            user_agent = serializer.validated_data.get("user_agent", "")
            if "device_type" not in serializer.validated_data:
                serializer.validated_data["device_type"] = detect_device_type(
                    user_agent
                )
            if "browser" not in serializer.validated_data:
                serializer.validated_data["browser"] = detect_browser(
                    user_agent)

            session, result = TrackingService.start_session(
                domain, serializer.validated_data
            )

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageViewAPI(APIView):
    """
    Purpose: Track when a user views a specific page on a website.

    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PageViewSerializer(data=request.data)
        if serializer.is_valid():
            # extract fileds
            domain = serializer.validated_data.pop("domain")
            session_id = serializer.validated_data.pop("session_id")

            # Add client info if not provided
            client_info = get_client_info(request)
            if "user_agent" not in serializer.validated_data:
                serializer.validated_data["user_agent"] = client_info["user_agent"]
            if "ip_address" not in serializer.validated_data:
                serializer.validated_data["ip_address"] = client_info["ip_address"]

            # Record the page view via the service layer
            result = TrackingService.record_pageview(
                domain, session_id, serializer.validated_data
            )

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data.pop("domain")
            session_id = serializer.validated_data.pop("session_id")
            serializer.validated_data.pop("user_agent", None)
            serializer.validated_data.pop("ip_address", None)
            result = TrackingService.record_event(
                domain, session_id, serializer.validated_data
            )

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionEndAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SessionEndSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data["domain"]
            session_id = serializer.validated_data["session_id"]

            result = TrackingService.end_session(domain, session_id)

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchTrackingAPI(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        data = request.data if isinstance(
            request.data, list) else [request.data]

        # Add client info to all items
        client_info = get_client_info(request)
        for item in data:
            if "user_agent" not in item:
                item["user_agent"] = client_info["user_agent"]
            if "ip_address" not in item:
                item["ip_address"] = client_info["ip_address"]
            if "country" not in item:
                item["country"] = client_info["country"]

            # Detect device type and browser
            user_agent = item.get("user_agent", "")
            if "device_type" not in item:
                item["device_type"] = detect_device_type(user_agent)
            if "browser" not in item:
                item["browser"] = detect_browser(user_agent)

        result = TrackingService.batch_track_events(data)

        if result["status"] == "partial":
            return Response(result, status=status.HTTP_207_MULTI_STATUS)
        return Response(result, status=status.HTTP_201_CREATED)
