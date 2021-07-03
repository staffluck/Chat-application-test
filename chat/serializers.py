from rest_framework.exceptions import ValidationError
from rest_framework import serializers

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
        dialog_id = self.context['request'].path.split('/')[-2]
        dialog = Dialog.objects.get(id=dialog_id)
        message = Message.objects.create(body=body, dialog=dialog, author=author)

        return message

    def validate(self, data):
        dialog_id = self.context['request'].path.split('/')[-2]
        if not Dialog.objects.filter(id=dialog_id).exists():
            raise ValidationError({"details": "Not found"}, 404)
        return data

    class Meta:
        model = Message
        exclude = ("dialog", )

        extra_kwargs = {
            "author": {
                "read_only": True
            }
        }
