from .views import RoleView
from django.urls import path

urlpatterns = [
    path('', RoleView.as_view()),
    path('<role_id>/', RoleView.as_view())
]
