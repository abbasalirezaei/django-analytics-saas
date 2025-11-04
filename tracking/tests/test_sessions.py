import pytest
import random
import string
from django.urls import reverse
from rest_framework.test import APITestCase

def generate_session_data():
    return {
        "domain": "example.com",
        "session_id": "".join(random.choices(string.ascii_lowercase + string.digits, k=16)),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "ip_address": "192.168.1.101",
        "country": "IR",
        "browser": "chrome",
        "device_type": "desktop",
    }

@pytest.mark.django_db
class SessionStartAPITest(APITestCase):
    def test_start_session_status_201(self):
        data = generate_session_data()
        url = reverse("tracking:api_v1:session-start")
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201