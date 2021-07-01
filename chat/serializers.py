from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Dialog


class DialogSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    users = serializers.ListField()
    user = serializers.CurrentUserDefault()

    def create(self, validated_data):
        user = validated_data['user']
        users_ids = validated_data['users']
        dialog = Dialog.objects.create()
        users_to_add = []

        for id_ in users_ids:
            user_to_add = User.objects.filter(id=id_)
            if user_to_add.exists():
                users_to_add.append(user_to_add)
        dialog.users.add(user, *users_to_add)

        return dialog

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return last_message

    class Meta:
        model = Dialog
        exclude = ("messages")
