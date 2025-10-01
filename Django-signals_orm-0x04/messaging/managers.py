from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_messages(self, user):
        return self.filter(receiver=user, is_read=False)