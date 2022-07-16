from django.db import models
from django.db.models import CASCADE, SET_NULL

from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState


class TelegramUser(AbstractTelegramUser):
    pass


class TelegramChat(AbstractTelegramChat):
    pass


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')


class ChatWebhook(models.Model):
    tg_user = models.ForeignKey(TelegramUser, related_name='chat_webhooks', on_delete=SET_NULL, null=True)
    tg_chat = models.ForeignKey(TelegramChat, related_name='chat_webhooks', on_delete=CASCADE)
    token = models.TextField(max_length=32, unique=True)
    last_used = models.DateTimeField(blank=True, null=True)
