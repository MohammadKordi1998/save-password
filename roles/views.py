from required.required import Required
from .models import RoleModel
from rest_framework import status
from message.Message import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, role_id=None):
        try:
            if role_id is None:
                roles = RoleModel.objects.order_by('-datetime_created').values()
                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    roles
                ).message()

            else:
                role = RoleModel.objects.filter(id=role_id).values()
                role = role[0] if len(role) > 0 else 'Not Found Role'

                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    role
                ).message()

        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()

        return Response(message, message['status_code'])

    def post(self, request):
        try:
            required = Required(
                {
                    'role_name': bool('role_name' in request.data)
                },
                {
                    'role_name': {
                        'type': 'string',
                        'min_len': 5,
                        'max_len': 100,
                        'unique': True
                    },
                }
            ).required()

            if len(required) > 0:
                return Response(
                    required,
                    status=status.HTTP_400_BAD_REQUEST
                )

            role_name = request.data['role_name']

            role = RoleModel.objects.create(
                role_name=role_name
            )

            message = Message(
                'ok',
                status.HTTP_200_OK,
                role.id
            ).message()

        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()

        return Response(message, message['status_code'])

    def put(self, request, role_id=None):
        try:
            required = Required(
                {
                    'role_name': bool('role_name' in request.data)
                },
                {
                    'role_name': {
                        'type': 'string',
                        'min_len': 5,
                        'max_len': 100,
                        'unique': True
                    },
                }
            ).required()

            if len(required) > 0:
                return Response(
                    required,
                    status=status.HTTP_400_BAD_REQUEST
                )
            role = RoleModel.objects.get(id=role_id)
            role_name = request.data['role_name']

            role.role_name = role_name
            role.save()

            message = Message(
                'ok',
                status.HTTP_200_OK,
                role.id
            ).message()

            return Response(message, status.HTTP_200_OK)

        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()

            return Response(message, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, role_id=None):
        try:
            role = RoleModel.objects.get(id=role_id)
            role.delete()

            message = Message(
                'ok',
                status.HTTP_200_OK,
                'Deleted'
            ).message()

        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()

        return Response(message, message['status_code'])
