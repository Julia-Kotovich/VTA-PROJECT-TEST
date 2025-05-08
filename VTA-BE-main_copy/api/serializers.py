from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Chat, LikeResponse,Feedback
class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200)


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = LikeResponse
        fields = '__all__'

class FeebackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'