from rest_framework.decorators import action
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


# Filters for searching and ordering
class ConversationFilter(filters.FilterSet):
    class Meta:
        model = Conversation
        fields = {
            'participants_id__username': ['exact', 'icontains'],
            'created_at': ['exact', 'lt', 'gt'],
        }

class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'conversation_id__conversation_id': ['exact'],
            'sender_id__username': ['exact', 'icontains'],
            'sent_at': ['exact', 'lt', 'gt'],
        }

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'user_id'
    lookup_value_regex = '[0-9]+'
    
    # Get serializer class for user
    def get_serializer_class(self):
        return UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'conversation_id'
    lookup_value_regex = '[0-9]+'
    
    # Get serializer class for conversation
    def get_serializer_class(self):
        return ConversationSerializer
    
    # Return only conversations where the user is a participant
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)
    
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
# Implement the endpoints to create a new conversation
@action(detail=False, methods=['post'])
def create_conversation(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'message_id'
    lookup_value_regex = '[0-9]+'
    
    # Get serializer class for message
    def get_serializer_class(self):
        return MessageSerializer
    
    # Return only messages in conversations where the user is a participant
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    # Implement the endpoints to create a new message
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    