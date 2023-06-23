from .models import RoleModel
from rest_framework import status
from message.Message import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RoleView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_all = RoleModel.objects.all()
        self.role = RoleModel.objects

    def get(self, request, role_id=None):
        try:
            if role_id is None:
                roles = self.role_all.values()
                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    roles
                ).message()
            else:
                role = self.role.get(id=role_id)
                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    {
                        'id': role.id,
                        'role_name': role.role_name,
                        'datetime_created': role.datetime_created
                    }
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
            if bool('role_name' in request.data):
                role_name = request.data['role_name']
                role = self.role.create(
                    role_name=role_name
                )

                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    role.id
                ).message()
            else:
                message = Message(
                    'Error',
                    status.HTTP_400_BAD_REQUEST,
                    {
                        'role_name': 'str(role_name)'
                    }
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
            if bool('role_name' in request.data):
                role_name = request.data['role_name']
                role = self.role.get(id=role_id)

                role.role_name = role_name
                role.save()

                message = Message(
                    'ok',
                    status.HTTP_200_OK,
                    role.id
                ).message()
            else:
                message = Message(
                    'Error',
                    status.HTTP_400_BAD_REQUEST,
                    {
                        'role_name': 'str(role_name)'
                    }
                ).message()
        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()

        return Response(message, message['status_code'])

    def delete(self, request, role_id=None):
        try:
            role = self.role.get(id=role_id)
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
