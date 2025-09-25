from rest_framework import permissions
from .models import Conversation, Message
from .auth import CustomJWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Custom permission to check if the user is a participant in the conversation
class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        elif isinstance(obj, Message):
            return request.user in obj.conversation_id.participants.all()
        return False
    
# Custom permission to only allow message sender or conversation participants to access messages.
class IsSenderOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return request.user == obj.sender_id or request.user in obj.conversation_id.participants.all()
        return False