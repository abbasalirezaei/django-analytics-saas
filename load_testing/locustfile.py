import random
import string

from locust import HttpUser, between, task


class BaseUser(HttpUser):
    """Base user class with common functionality"""

    abstract = True
    host = "http://web:8000"

    def login(self, username="test_user", password="test_password"):
        """Reusable login method"""
        response = self.client.post(
            "/api/accounts/v1/auth/login/",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            self.headers = {"Authorization": f"Bearer {response.json().get('access')}"}
            return True
        else:
            self.headers = {}
            print(f"Login failed: {response.status_code} - {response.text}")
            return False

    def generate_random_domain(self):
        """Generate random domain name"""
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        return f"testsite{random_suffix}.com"


class LoginUser(BaseUser):
    weight = 2
    wait_time = between(1, 3)

    def on_start(self):
        """Login when user starts"""
        self.login()
        self.created_websites = []

    @task(3)
    def get_websites(self):
        self.client.get("/api/accounts/v1/websites/", headers=self.headers)

    @task(2)
    def get_user_profile(self):
        self.client.get("/api/accounts/v1/user/profile/", headers=self.headers)

    @task(2)
    def get_organization_profile(self):
        self.client.get("/api/accounts/v1/organization/profile/", headers=self.headers)

    @task(1)
    def regenerate_api_key(self):
        self.client.post(
            "/api/accounts/v1/organization/regenerate-api-key/", headers=self.headers
        )

    @task(2)
    def list_users(self):
        self.client.get("/api/accounts/v1/users/", headers=self.headers)

    @task(1)
    def create_website(self):
        domain = self.generate_random_domain()
        response = self.client.post(
            "/api/accounts/v1/websites/",
            json={"name": f"Test Website {domain}", "domain": domain},
            headers=self.headers,
        )
        if response.status_code == 201:
            self.created_websites.append(domain)
            return domain
        return None


class TrackingUser(BaseUser):
    weight = 3
    wait_time = between(1, 5)

    def on_start(self):
        """Login and setup tracking user"""
        if self.login():
            self.setup_tracking_data()

    def setup_tracking_data(self):
        """Setup initial tracking data"""
        self.current_domain = None
        self.active_sessions = []

        # Get or create a website for tracking
        response = self.client.get("/api/accounts/v1/websites/", headers=self.headers)
        if response.status_code == 200:
            websites = response.json()
            if isinstance(websites, list) and len(websites) > 0:
                self.current_domain = websites[0].get("domain")
                print(f"✅ TrackingUser using existing website: {self.current_domain}")
            else:
                print(" No websites found, creating new one...")
                self.current_domain = self.create_website()
        else:
            print(f"❌ Failed to get websites: {response.status_code}")
            self.current_domain = self.create_website()

    def create_website(self):
        """Create a website for tracking"""
        domain = self.generate_random_domain()
        response = self.client.post(
            "/api/accounts/v1/websites/",
            json={"name": f"Tracking Test {domain}", "domain": domain},
            headers=self.headers,
        )
        if response.status_code == 201:
            print(f"✅ Created new website: {domain}")
            return domain
        else:
            print(f"❌ Failed to create website: {response.status_code}")
            # Fallback to a default domain if creation fails
            return f"fallback-{random.randint(1000, 9999)}.com"

    def generate_session_data(self):
        """Generate realistic session data"""
        return {
            "session_id": "".join(
                random.choices(string.ascii_lowercase + string.digits, k=16)
            ),
            "user_agent": random.choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                ]
            ),
            "ip_address": f"192.168.1.{random.randint(100, 200)}",
            "country": random.choice(["US", "GB", "DE", "FR", "JP", "IR", "CA", "AU"]),
            "browser": random.choice(["chrome", "firefox", "safari", "edge", "opera"]),
            "device_type": random.choice(["desktop", "mobile", "tablet"]),
            "screen_resolution": random.choice(
                ["1920x1080", "1366x768", "1536x864", "1440x900", "375x812"]
            ),
        }

    def generate_pageview_data(self, session_id):
        """Generate realistic pageview data"""
        pages = [
            {"url": "/", "title": "Home Page"},
            {"url": "/about", "title": "About Us"},
            {"url": "/products", "title": "Our Products"},
            {"url": "/contact", "title": "Contact Us"},
            {"url": "/blog", "title": "Blog"},
            {"url": "/pricing", "title": "Pricing"},
            {"url": "/faq", "title": "FAQ"},
            {"url": "/services", "title": "Services"},
        ]
        page = random.choice(pages)

        return {
            "domain": self.current_domain,
            "session_id": session_id,
            "page_url": page["url"],
            "page_title": page["title"],
            "referrer": random.choice(
                [
                    "",
                    "https://google.com",
                    "https://facebook.com",
                    "https://twitter.com",
                    "https://linkedin.com",
                ]
            ),
            "load_time": random.uniform(0.5, 3.0),
            "user_agent": random.choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                ]
            ),
            "ip_address": f"192.168.1.{random.randint(100, 200)}",
        }

    def generate_event_data(self, session_id):
        """Generate realistic event data that matches the API format"""
        events = [
            {
                "name": "button_click",
                "data": {
                    "button_id": "cta-signup",
                    "button_text": "Sign Up Now",
                    "page_section": "header",
                },
            },
            {
                "name": "button_click",
                "data": {
                    "button_id": "buy-now",
                    "button_text": "Buy Now",
                    "page_section": "product",
                },
            },
            {
                "name": "form_submit",
                "data": {
                    "form_id": "contact-form",
                    "form_type": "contact",
                    "field_count": 4,
                },
            },
            {
                "name": "form_submit",
                "data": {
                    "form_id": "newsletter-signup",
                    "form_type": "subscription",
                    "field_count": 1,
                },
            },
            {
                "name": "video_play",
                "data": {
                    "video_id": "intro-video",
                    "video_title": "Product Introduction",
                    "duration_seconds": 120,
                },
            },
            {
                "name": "download",
                "data": {
                    "file_name": "whitepaper.pdf",
                    "file_type": "pdf",
                    "file_size": "2.5MB",
                },
            },
            {
                "name": "link_click",
                "data": {
                    "link_url": "/features",
                    "link_text": "Learn More",
                    "link_type": "internal",
                },
            },
            {
                "name": "add_to_cart",
                "data": {
                    "product_id": f"prod_{random.randint(1000, 9999)}",
                    "product_name": f"Product {random.randint(1, 100)}",
                    "price": round(random.uniform(10, 100), 2),
                    "quantity": random.randint(1, 3),
                },
            },
            {
                "name": "product_view",
                "data": {
                    "product_id": f"prod_{random.randint(1000, 9999)}",
                    "product_name": f"Product {random.randint(1, 100)}",
                    "category": random.choice(
                        ["electronics", "clothing", "books", "home"]
                    ),
                },
            },
        ]

        event = random.choice(events)
        pages = [
            "/",
            "/home",
            "/products",
            "/products/item-1",
            "/about",
            "/contact",
            "/blog",
            "/pricing",
        ]

        return {
            "domain": self.current_domain,
            "session_id": session_id,
            "event_name": event["name"],
            "event_data": event["data"],
            "page_url": random.choice(pages),
            "user_agent": random.choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                ]
            ),
            "ip_address": f"192.168.1.{random.randint(100, 200)}",
        }

    def generate_batch_data(self):
        """Generate batch tracking data with proper event format"""
        session_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=16)
        )

        # Start session
        session_data = self.generate_session_data()
        session_data["session_id"] = session_id
        session_data["domain"] = self.current_domain

        # Generate multiple pageviews
        pageviews = []
        for _ in range(random.randint(2, 5)):
            pageview_data = self.generate_pageview_data(session_id)
            pageviews.append({"type": "pageview", "data": pageview_data})

        # Generate multiple events with correct format
        events = []
        for _ in range(random.randint(1, 3)):
            event_data = self.generate_event_data(session_id)
            events.append({"type": "event", "data": event_data})

        return {
            "session_start": session_data,
            "pageviews": pageviews,
            "events": events,
            "session_end": {"domain": self.current_domain, "session_id": session_id},
        }

    # TRACKING TASKS - All endpoints from your URLs
    @task(4)
    def start_session(self):
        """Start a new tracking session - /api/tracking/v1/session/start/"""
        if not self.current_domain:
            self.setup_tracking_data()
            if not self.current_domain:
                return

        session_data = self.generate_session_data()
        session_data["domain"] = self.current_domain

        response = self.client.post(
            "/api/tracking/v1/session/start/", json=session_data, headers=self.headers
        )

        if response.status_code == 201:
            self.active_sessions.append(session_data["session_id"])
            print(f"✅ Started session: {session_data['session_id']}")
            return session_data["session_id"]
        else:
            print(f"❌ Failed to start session: {response.status_code}")
        return None

    @task(6)  # Most frequent - pageviews happen a lot
    def track_pageview(self):
        """Track a pageview - /api/tracking/v1/pageview/"""
        if not self.current_domain:
            return

        # Use existing session or create new one
        if not self.active_sessions:
            session_id = self.start_session()
            if not session_id:
                return
        else:
            session_id = random.choice(self.active_sessions)

        pageview_data = self.generate_pageview_data(session_id)

        response = self.client.post(
            "/api/tracking/v1/pageview/", json=pageview_data, headers=self.headers
        )

        if response.status_code == 201:
            print(f"✅ Tracked pageview for session: {session_id}")
        else:
            print(f"❌ Failed to track pageview: {response.status_code}")

    @task(5)
    def track_event(self):
        """Track an event - /api/tracking/v1/event/"""
        if not self.current_domain:
            print("❌ No domain available for event tracking")
            return

        # Use existing session or create new one
        if not self.active_sessions:
            session_id = self.start_session()
            if not session_id:
                print("❌ Failed to create session for event tracking")
                return
        else:
            session_id = random.choice(self.active_sessions)

        event_data = self.generate_event_data(session_id)

        print(f"📤 Sending event: {event_data['event_name']} for session {session_id}")

        try:
            response = self.client.post(
                "/api/tracking/v1/event/", json=event_data, headers=self.headers
            )

            if response.status_code == 201:
                print(f"✅ Successfully tracked event '{event_data['event_name']}'")
            else:
                print(
                    f"❌ Event tracking failed: {response.status_code} - {response.text}"
                )
                # Print the exact data that was sent for debugging
                print(f"🔍 Data sent: {event_data}")

        except Exception as e:
            print(f"🚨 Exception during event tracking: {e}")

    @task(2)
    def end_session(self):
        """End an active session - /api/tracking/v1/session/end/"""
        if not self.current_domain or not self.active_sessions:
            return

        session_id = random.choice(self.active_sessions)
        response = self.client.post(
            "/api/tracking/v1/session/end/",
            json={"domain": self.current_domain, "session_id": session_id},
            headers=self.headers,
        )

        if response.status_code == 200:
            self.active_sessions.remove(session_id)
            print(f"✅ Ended session: {session_id}")
        else:
            print(f"❌ Failed to end session: {response.status_code}")

    @task(1)  # Less frequent - batch operations
    def batch_tracking(self):
        """Send batch tracking data - /api/tracking/v1/batch/"""
        if not self.current_domain:
            return

        batch_data = self.generate_batch_data()

        response = self.client.post(
            "/api/tracking/v1/batch/", json=batch_data, headers=self.headers
        )

        if response.status_code == 201:
            # Add the session from batch to active sessions
            session_id = batch_data["session_start"]["session_id"]
            self.active_sessions.append(session_id)
            print(f"✅ Sent batch tracking data with session: {session_id}")
        else:
            print(f"❌ Failed to send batch data: {response.status_code}")


class AnalyticsUser(BaseUser):
    weight = 2
    wait_time = between(2, 5)

    def on_start(self):
        """Login and setup analytics user"""
        if self.login():
            self.website_id = self.get_or_create_website()

    def get_or_create_website(self):
        """Get existing website or create new one for analytics"""
        response = self.client.get("/api/accounts/v1/websites/", headers=self.headers)
        if response.status_code == 200:
            websites = response.json()
            # FIX: Check if websites is a list and not empty
            if isinstance(websites, list) and len(websites) > 0:
                website_id = websites[0].get("id")
                print(f"✅ AnalyticsUser using existing website ID: {website_id}")
                return website_id
            else:
                print(" No websites found for analytics, creating new one...")

        # Create new website if none exists
        domain = self.generate_random_domain()
        response = self.client.post(
            "/api/accounts/v1/websites/",
            json={"name": f"Analytics Test {domain}", "domain": domain},
            headers=self.headers,
        )
        if response.status_code == 201:
            website_id = response.json().get("id")
            print(f"✅ Created new website for analytics: {website_id}")
            return website_id
        else:
            print(f"❌ Failed to create website for analytics: {response.status_code}")
            return None

    @task(4)
    def get_overview(self):
        if self.website_id:
            self.client.get(
                f"/api/reporting/v1/overview/?days=7&website_id={self.website_id}",
                headers=self.headers,
            )
        else:
            print(" AnalyticsUser: No website_id available for overview")

    @task(3)
    def get_timeseries(self):
        if self.website_id:
            periods = random.choice([1, 7, 30])
            self.client.get(
                f"/api/reporting/v1/timeseries/?days={periods}&website_id={self.website_id}",
                headers=self.headers,
            )

    @task(3)
    def get_top_pages(self):
        if self.website_id:
            limit = random.choice([5, 10, 20])
            self.client.get(
                f"/api/reporting/v1/top-pages/?days=7&limit={limit}&website_id={self.website_id}",
                headers=self.headers,
            )

    @task(2)
    def get_event_summary(self):
        if self.website_id:
            self.client.get(
                f"/api/reporting/v1/events/?days=7&website_id={self.website_id}",
                headers=self.headers,
            )

    @task(1)
    def get_realtime_stats(self):
        if self.website_id:
            self.client.get(
                f"/api/reporting/v1/realtime/?website_id={self.website_id}",
                headers=self.headers,
            )
