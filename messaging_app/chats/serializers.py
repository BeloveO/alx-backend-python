from rest_framework import serializers
from .models import User, Conversation, Message

# Serializers for the User, Conversation, and Message models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    # Nested serializer to include participant details
    participants = UserSerializer(many=True, read_only=True)
    # Nested representation to validate errors in the participants
    def validate_participants(self, value):
        if not value:
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return value
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    # Nested serializer to include sender and message details
    sender = UserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)
    message = serializers.CharField(source='message_body')
    # Nested representation to validate errors in the message body
    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    class Meta:
        model = Message
        fields = ['message_id', 'conversation_id', 'sender_id', 'message', 'sent_at']