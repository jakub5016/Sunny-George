from rest_framework import serializers

class TextChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_blank=True)
    session_id = serializers.UUIDField(required=False)
    start = serializers.BooleanField(required=False, default=False)
    locale = serializers.ChoiceField(choices=["pl", "en"], required=False, default="pl")