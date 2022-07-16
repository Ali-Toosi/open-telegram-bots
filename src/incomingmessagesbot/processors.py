from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string

from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState, ChatWebhook
from .bot import TelegramBot


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def start(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/start':
        bot.sendMessage(update.get_chat().get_id(), '/add_webhook or /delete_all_webhooks')


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def add_webhook(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text != '/add_webhook':
        return

    webhook = ChatWebhook(
        tg_user=state.telegram_user,
        tg_chat=state.telegram_chat
    )
    token = None
    while not token:
        token = get_random_string(32)
        if ChatWebhook.objects.filter(token=token).exists():
            token = None
    webhook.token = token
    webhook.save()
    bot.sendMessage(update.get_chat().get_id(), f"""
        Token created for this chat.
Send your messages to https://{settings.DOMAIN_NAME}{reverse("incomingmessagesbot:incoming_message_webhook", args=(webhook.token,))}
    """)


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text, success='sure_delete', fail=state_types.Keep)
def delete_all_webhooks(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text != '/delete_all_webhooks':
        raise ProcessFailure

    bot.sendMessage(update.get_chat().get_id(), "Are you sure you want to delete all webhooks? Cannot be reverted.")


@processor(state_manager, from_states='sure_delete', message_types=message_types.Text, success='', fail='')
def delete_all_webhooks_confirm(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if str(text).lower() in ['yes', 'y']:
        ChatWebhook.objects.filter(tg_chat=state.telegram_chat).delete()
        bot.sendMessage(update.get_chat().get_id(), "All webhooks deleted.")
    else:
        bot.sendMessage(update.get_chat().get_id(), "That's what I thought.")
