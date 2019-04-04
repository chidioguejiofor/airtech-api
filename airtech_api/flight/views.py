from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from ..utils.helpers.json_helpers import generate_response, raise_error
from .serializers import FlightSerializer
from ..utils.error_messages import serialization_errors
from ..utils.validators.token_validator import AdminTokenvalidator
from ..utils import success_messages


class FlightView(APIView):

    permission_classes = [AdminTokenvalidator]
    protected_methods = ['POST']

    def post(self, request, format='json'):
        """Creates a new flight

        Args:
            request: An object that contains the request made by the user
            format(str): Specifies that JSON is sent to the app

        Returns:
            None

        """
        user = request.decoded_user
        request_data = dict(**request.data, createdBy=user.id)
        serializer = FlightSerializer(data=request_data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            return generate_response(
                serializer.data,
                success_messages['resource_created'].format('Flight'),
                status_code=HTTP_201_CREATED)
        raise_error(
            serialization_errors['many_invalid_fields'],
            err_dict=serializer.errors)
