from .models import Users
from django.db.models import Q, F
from roles.models import RoleModel
from rest_framework import status
from message.Message import Message
from required.required import Required
from .serializer import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.annotate_key = dict(
            role_name=F('role__role_name')
        )
        self.values = ['id', 'first_name', 'last_name', 'username', 'role_name', 'datetime_created']

    def get(self, request, pk=None):
        try:

            if pk is None:
                users = Users.objects.filter(is_active=True).annotate(**self.annotate_key).values(*self.values)
                message = Message(
                    'OK',
                    status.HTTP_200_OK,
                    users
                ).message()
                return Response(message, status=status.HTTP_200_OK)

            else:
                user = Users.objects.filter(id=pk, is_active=True).annotate(**self.annotate_key).values(*self.values)
                status_code = status.HTTP_200_OK if len(user) > 0 else status.HTTP_404_NOT_FOUND
                user = user[0] if len(user) > 0 else 'Not Found User'
                message = Message(
                    'OK',
                    status_code,
                    user
                ).message()
                return Response(message, status=status_code)

        except Exception as ex:
            message = Message(
                'Error',
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])

    def post(self, request):
        try:
            required = Required(
                {
                    'first_name': bool('first_name' in request.data),
                    'last_name': bool('last_name' in request.data),
                    'username': bool('username' in request.data),
                    'role': bool(RoleModel.objects.filter(Q(role_name='user') | Q(role_name='User'))),
                    'password': bool('password' in request.data)
                },
                {
                    'first_name': {'type': 'string', 'min_len': 5, 'max_len': 100, 'unique': False},
                    'last_name': {'type': 'string', 'min_len': 5, 'max_len': 100, 'unique': False},
                    'username': {'type': 'string', 'min_len': 5, 'max_len': 100, 'unique': True},
                    'role': 'Not Found',
                    'password': {'type': 'string', 'min_len': 5, 'max_len': 20, 'unique': False},
                }
            ).required()

            if len(required) > 0:
                return Response(required, status=status.HTTP_400_BAD_REQUEST)

            UserSerializer.first_name = request.data['first_name']
            UserSerializer.last_name = request.data['last_name']
            UserSerializer.username = request.data['username']
            UserSerializer.role_id = RoleModel.objects.get(Q(role_name='user') | Q(role_name='User')).id
            UserSerializer.password = request.data['password']

            required = Required(
                {
                    'username': not bool(Users.objects.filter(username=UserSerializer.username))
                },
                {
                    'username': 'The UserName is Duplicate'
                }
            ).required()

            if len(required) > 0:
                return Response(required, status=status.HTTP_400_BAD_REQUEST)

            user = Users.objects.create_user(
                first_name=UserSerializer.first_name,
                last_name=UserSerializer.last_name,
                username=UserSerializer.username,
                role_id=UserSerializer.role_id,
                password=UserSerializer.password,
            )

            Token.objects.create(user=user)

            message = Message(
                "Create",
                status.HTTP_200_OK,
                user.id
            ).message()

            return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Error",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
            user.is_active = False
            user.save()

            message = Message(
                "Delete",
                status.HTTP_200_OK,
                "The Deletion was Successful"
            ).message()

            return Response(message, status=status.HTTP_200_OK)

        except Exception as ex:
            message = Message(
                "Failed",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        try:
            required = Required(
                {
                    'username': bool('username' in request.data),
                    'password': bool('password' in request.data)
                },
                {
                    'username': "Request username does not exist",
                    'password': "Request password does not exist",
                }
            ).required()

            if len(required) > 0:
                return Response(required, status=status.HTTP_400_BAD_REQUEST)

            object_login = dict(
                username=request.data['username'],
                password=request.data['password']
            )

            user = authenticate(**object_login)

            if user is not None:
                message = Message(
                    "Token",
                    status.HTTP_200_OK,
                    user.auth_token.key
                ).message()
                return Response(message, status=message['status_code'])

            else:
                message = Message(
                    "UNAUTHORIZED",
                    status.HTTP_401_UNAUTHORIZED,
                    "").message()

                return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Not Found User or Role",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])


class ChangeRoleUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = Users.objects.get(id=pk, is_active=True)
            role = RoleModel.objects.get(id=request.data['roleId'])
            # user.is_staff = 1
            user.role_id = role.id
            user.save()
            message = Message(
                "Change Role",
                status.HTTP_200_OK,
                {"role ": user.role.role_name, 'user': user.username}
            ).message()
            return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Not Found User or Role",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])
