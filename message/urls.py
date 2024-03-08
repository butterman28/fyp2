from django.urls import path, re_path
from .views import *
from . import views
from djmoney.models.fields import *

app_name = "message"

urlpatterns = [
    path(
        "send-message/<str:receiver_username>/",
        SendMessageView.as_view(),
        name="send_message",
    ),
]
