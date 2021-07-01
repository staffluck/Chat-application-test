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
        users_to_add = []

        for user_ in users:
            users_to_add.append(user_)
        dialog.users.add(user, *users_to_add)

        return dialog

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return last_message.body
        return ""

    class Meta:
        model = Dialog
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        body = validated_data['body']
        dialog = validated_data['dialog']
        message = Message.objects.create(body=body, dialog=dialog)

        return message

    class Meta:
        model = Message
        exclude = ('author', )
