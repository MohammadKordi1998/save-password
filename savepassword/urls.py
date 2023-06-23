from django.urls import path
from .views import SavePasswordView

urlpatterns = [
    path('', SavePasswordView.as_view()),
    path('<pk>/', SavePasswordView.as_view())
]
