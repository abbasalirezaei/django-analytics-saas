from locust import HttpUser, task, between


class LoginUser(HttpUser):
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

    """
        we don't need this task right now because we add on_start method to login once
        @task
        def login(self):
            response = self.client.post("/api/accounts/v1/auth/login/", json={
                "username": "test_user",
                "password": "test_password"
            })

            if response.status_code == 200:
                token = response.json().get("access")
                self.headers = {"Authorization": f"Bearer {token}"}
                print("Login successful")
            else:
                self.headers = {}
                print(f"Login failed ({response.status_code}): {response.text}")

    """

    @task
    def get_websites(self):
        self.client.get('/api/accounts/v1/websites/', headers=self.headers)
