"""Locust file"""
import json
from locust import HttpLocust, TaskSet, task

# from processors.default_report_processor import DefaultReportingProcessor
# prof, _ = Portfolio.objects.get_or_create(name='prof', display_name='Professor', active_date='2013-01-01')
# Portfolio.objects.filter(name='prof').delete(force=True)
# data_set = DataSet.objects.create(portfolio=prof, platform=fb_platform, manual_name='Test 10-1-')


# DefaultReportingProcessor.create_default_report(
#     prof,
#     Platform.objects.get(short_name='OFB')
# )
class FlightTaskSet(TaskSet):
    """Booking Actions."""

    auth_token = ''
    flight_id = ''

    def on_start(self):
        """Method to run on start."""
        response = self.client.post(
            '/auth/login',
            json={
                "usernameOrEmail": "regulartest@email.com",
                "password": "password"
            },
            headers={'Content-Type': 'application/json'})
        self.auth_token = json.loads(response.text)['data']['token']

        response = self.client.post(
            '/auth/login',
            json={
                "usernameOrEmail": "regularadmintest@email.com",
                "password": "password"
            },
            headers={'Content-Type': 'application/json'})
        self.admin_token = json.loads(response.text)['data']['token']

    @task
    def created_flight(self):
        data = {
            "capacity": 70,
            "location": "Popo York",
            "destination": "Lagos, Nigeria",
            "schedule": "2019-10-10 14:00:01",
            "currentPrice": 4000,
            "type": "international"
        }

        response = self.client.post(
            '/flights',
            json=data,
            headers={'Authorization': 'Bearer ' + self.admin_token})

        self.flight_id = json.loads(response.text)['data']['id']

    @task
    def get_flight(self):
        """Task to get user filghts."""
        self.client.get(f'/flights/{self.flight_id}',
                        headers={'Authorization': 'Bearer ' + self.auth_token})

    @task
    def get_flights(self):
        """Task to get user filghts."""
        self.client.get('/flights',
                        headers={'Authorization': 'Bearer ' + self.auth_token})


class ApplicationUser(HttpLocust):
    """Locust analyze."""

    task_set = FlightTaskSet
    min_wait = 0
    max_wait = 0
    host = "http://127.0.0.1:8000/api/v1"
