from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
import logging
from django.utils import timezone

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

# Log the old content of a message into a separate MessageHistory model before it’s updated.
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            history = MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            # Update message edited fields
            Message.objects.filter(pk=instance.pk).update(edited=True, edited_by=instance.sender)
            instance.edited = True
            instance.edited_by = instance.sender
            logger.info(f"Message {instance.message_id} edited. Old content logged.")