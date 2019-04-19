from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import (not_found_errors)


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def catch_all(request):
    return Response({'message': not_found_errors['resource_not_found']},
                    status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def welcome_message(request):
    return Response({'message': success_messages['welcome_message']})


# @api_view(['POST', 'PATCH', 'DELETE', 'PUT'])
# def test(request):
#
#     template = get_template('confirm-email.html')
#     html_content = template.render({'confirm_link': 'https://faceboook.com'})
#     mail_dict = {
#         'subject': 'Now we are talking',
#         'receiver': 'chidioguejiofor@gmail.com',
#         'body': html_content,
#     }
#
#     # import pdb; pdb.set_trace()
#     send_mail_as_html(**mail_dict)
#     return Response({'message': success_messages['welcome_message']})
