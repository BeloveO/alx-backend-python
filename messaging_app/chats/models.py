from django.db import models

# Create your models here.

class User(models.Model):
    # extension of the Abstract user for values not defined in the built-in Django User model
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    password_hash = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(default=models.functions.Now())


class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    participants_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=models.functions.Now())

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=models.functions.Now())