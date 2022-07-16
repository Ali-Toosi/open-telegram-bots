from django.urls import path
from .views import handle_bot_request, poll_updates, incoming_message

app_name = "incomingmessagesbot"
urlpatterns = [
    path('update/', handle_bot_request),
    path('poll/', poll_updates),
    path('<slug:token>/', incoming_message, name="incoming_message_webhook")
]
