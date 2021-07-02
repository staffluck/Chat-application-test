from django.db import models
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Dialog(models.Model):
    users = models.ManyToManyField(User, related_name="dialogs", db_index=True)
    title = models.CharField(max_length=60, null=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="messages", db_index=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    body = models.TextField()
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return "{}: {}".format(self.id, self.body)

    def notify_socket(self):

        notification = {
            "type": "chat_message",
            "message": {"body": self.body, "dialog_id": self.dialog.id, "author": self.author.id}
        }

        layer = get_channel_layer()

        for user in self.dialog.users.all():
            async_to_sync(layer.group_send)("{}".format(user.id), notification)

    def save(self, *args, **kwargs):
        is_new = self.id
        self.body = self.body.strip()
        super().save(*args, **kwargs)
        if is_new is None:
            self.notify_socket()

    class Meta:
        ordering = ('-timestamp', )
