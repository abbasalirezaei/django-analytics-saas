from locust import HttpUser, task, between
import random
import string


class LoginUser(HttpUser):
    weight = 1
    wait_time = between(1, 3)
    host = "http://web:8000"

    def on_start(self):
        response = self.client.post("/api/accounts/v1/auth/login/", json={
            "username": "test_user",
            "password": "test_password"
        })
        if response.status_code == 200:
            token = response.json().get("access")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task
    def get_websites(self):
        self.client.get('/api/accounts/v1/websites/', headers=self.headers)

    @task
    def get_user_profile(self):
        self.client.get('/api/accounts/v1/user/profile/', headers=self.headers)

    @task
    def get_organization_profile(self):
        self.client.get('/api/accounts/v1/organization/profile/', headers=self.headers)

    @task
    def regenerate_api_key(self):
        response = self.client.post('/api/accounts/v1/organization/regenerate-api-key/', headers=self.headers)
        if response.status_code == 200:
            self.api_key = response.json().get('new_api_key', None)
        else:
            self.api_key = {}

    @task
    def list_users(self):
        self.client.get('/api/accounts/v1/users/', headers=self.headers)

    @task
    def create_website(self):
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        domain = f"testsite{random_suffix}.com"
        response = self.client.post(
            '/api/accounts/v1/websites/',
            json={
                'name': f'Test Website {random_suffix}',
                'domain': domain
            },
            headers=self.headers
        )
        if response.status_code == 201:
            self.last_created_domain = domain
            return domain
        else:
            return None


class AnalyticsUser(HttpUser):
    weight = 1
    wait_time = between(1, 3)
    host = "http://web:8000"

    def on_start(self):
        response = self.client.post("/api/accounts/v1/auth/login/", json={
            "username": "test_user",
            "password": "test_password"
        })
        if response.status_code == 200:
            token = response.json().get("access")
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            self.website_id = self.get_website_id()
        else:
            self.headers = {}
            self.website_id = None

    def get_website_id(self):
        response = self.client.get("/api/accounts/v1/websites/", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                return data[0].get("id")
            else:
                return self.create_website_for_analytics()
        return None

    def create_website_for_analytics(self):
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        domain = f"analytics-site{random_suffix}.com"
        response = self.client.post(
            '/api/accounts/v1/websites/',
            json={
                'name': f'Analytics Test Website {random_suffix}',
                'domain': domain
            },
            headers=self.headers
        )
        if response.status_code == 201:
            return response.json().get("id")
        return None

    @task(3)
    def get_overview(self):
        if self.website_id:
            self.client.get(f"/api/reporting/v1/overview/?days=7&website_id={self.website_id}", headers=self.headers)

    @task(2)
    def get_timeseries(self):
        if self.website_id:
            self.client.get(f"/api/reporting/v1/timeseries/?days=7&website_id={self.website_id}", headers=self.headers)

    @task(2)
    def get_top_pages(self):
        if self.website_id:
            self.client.get(f"/api/reporting/v1/top-pages/?days=7&limit=10&website_id={self.website_id}", headers=self.headers)

    @task(1)
    def get_event_summary(self):
        if self.website_id:
            self.client.get(f"/api/reporting/v1/events/?days=7&website_id={self.website_id}", headers=self.headers)

    @task(1)
    def get_realtime_stats(self):
        if self.website_id:
            self.client.get(f"/api/reporting/v1/realtime/?website_id={self.website_id}", headers=self.headers)