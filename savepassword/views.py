import string
import secrets

from django.db.models import F
from rest_framework import status
from message.Message import Message
from .models import SavePasswordModel
from rest_framework.views import APIView
from .serializer import SPasswordSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SavePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.annotate_key = dict(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
        )
        self.values = ['id', 'site', 'username', 'password', 'first_name', 'last_name', 'datetime_created',
                       'datetime_updated']

    def get(self, reqeust, pk=None):
        try:
            user_id = reqeust.user.id

            if pk is None:
                all_save_password = SavePasswordModel.objects.filter(user_id=user_id) \
                    .annotate(**self.annotate_key).values(*self.values)

                message = Message(
                    "OK",
                    status.HTTP_200_OK,
                    all_save_password
                ).message()
                return Response(message, status=message['status_code'])

            else:
                save_password = SavePasswordModel.objects.filter(user_id=user_id, id=pk) \
                    .annotate(**self.annotate_key).values(*self.values)

                save_password = save_password[0] if len(save_password) > 0 else 'Not Found'

                message = Message(
                    "OK",
                    status.HTTP_200_OK,
                    save_password
                ).message()
                return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Error",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])

    def post(self, request):
        try:
            user_id = request.user.id
            SPasswordSerializer.site = request.data['site']
            SPasswordSerializer.username = request.data['username']
            SPasswordSerializer.is_random_pass = request.data['is_random_pass']
            SPasswordSerializer.user_id = user_id

            if SPasswordSerializer.is_random_pass:
                SPasswordSerializer.password_len = request.data['password_len']
                letters = string.ascii_letters
                digits = string.digits
                special_chars = '!@#$%&_-'

                alphabet = letters + digits + special_chars

                pwd_length = int(SPasswordSerializer.password_len)

                pwd = ''
                for i in range(pwd_length):
                    pwd += ''.join(secrets.choice(alphabet))

                SPasswordSerializer.password = pwd
            else:
                SPasswordSerializer.password = request.data['password']

            sp = SavePasswordModel.objects.create(
                site=SPasswordSerializer.site,
                username=SPasswordSerializer.username,
                password=SPasswordSerializer.password,
                user_id=SPasswordSerializer.user_id,
            )
            message = Message(
                "OK",
                status.HTTP_200_OK,
                sp.id
            ).message()

            return Response(message, status=message['status_code'])


        except Exception as ex:
            message = Message(
                "Error",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])

    def put(self, request, pk=None):
        try:
            user_id = request.user.id
            sp = SavePasswordModel.objects.get(id=pk, user_id=user_id)

            SPasswordSerializer.site = request.data['site']
            SPasswordSerializer.username = request.data['username']
            SPasswordSerializer.is_random_pass = request.data['is_random_pass']

            if SPasswordSerializer.is_random_pass:
                SPasswordSerializer.password_len = request.data['password_len']
                letters = string.ascii_letters
                digits = string.digits
                special_chars = '!@#$%&_-'

                alphabet = letters + digits + special_chars

                pwd_length = int(SPasswordSerializer.password_len)

                pwd = ''
                for i in range(pwd_length):
                    pwd += ''.join(secrets.choice(alphabet))

                SPasswordSerializer.password = pwd
            else:
                SPasswordSerializer.password = request.data['password']

            sp.site = SPasswordSerializer.site
            sp.username = SPasswordSerializer.username
            sp.password = SPasswordSerializer.password

            sp.save()

            message = Message(
                "OK",
                status.HTTP_200_OK,
                sp.id
            ).message()

            return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Error",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])

    def delete(self, request, pk=None):
        try:
            user_id = request.user.id
            sp = SavePasswordModel.objects.get(id=pk, user_id=user_id)
            sp.delete()
            message = Message(
                "OK",
                status.HTTP_200_OK,
                'Deleted'
            ).message()

            return Response(message, status=message['status_code'])

        except Exception as ex:
            message = Message(
                "Error",
                status.HTTP_400_BAD_REQUEST,
                f'{ex}'
            ).message()
            return Response(message, status=message['status_code'])
