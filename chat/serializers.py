from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Dialog, Message


class DialogSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data['user']
        users = validated_data['users']
        dialog = Dialog.objects.create(title=validated_data['title'])
        dialog.users.add(user, *users)

        return dialog

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return last_message.body
        return ""

    class Meta:
        model = Dialog
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        author = validated_data['user']
        body = validated_data['body']
        dialog = validated_data['dialog']
        message = Message.objects.create(body=body, dialog=dialog, author=author)

        return message

    class Meta:
        model = Message
        exclude = ('author', )
