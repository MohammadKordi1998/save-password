from django.urls import path
from .views import UserView, Login

urlpatterns = [
    path('', UserView.as_view()),
    path('login/', Login.as_view()),
    path('<pk>/', UserView.as_view()),
]
