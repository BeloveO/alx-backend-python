from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='message'
        )
        logger.info(f"Notification created for user {instance.receiver.username} about message {instance.message_id}")

@receiver(post_save, sender=Message)
def handle_new_messages(sender, instance, created, **kwargs):
    if created:
        create_notification(instance)
        logger.info(f"Handled new message from {instance.sender.username} to {instance.receiver.username}")