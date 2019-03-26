# from rest_framework import status
import pytest
from airtech_api.utils.success_messages import index_route
from airtech_api.utils.error_messages import not_found_errors

# Create your tests here.


class TestIndexRoute:
    """
    Tests the index routes
    """

    def test_welcome_endpoint_succeeds(self, client):
        """Should return a welcome message to the user on GET /api


        Returns:
            None
        """
        response = client.get('/api')
        data = response.data
        assert response.status_code == 200
        assert data['message'] == index_route['welcome_message']

    def test_invalid_route_fails(self, client):
        """Should fail when the specified route is invalid

       Returns:
           None
       """
        response = client.get('/invalid-route')
        data = response.data
        assert response.status_code == 404
        assert data['message'] == not_found_errors['resource_not_found']
