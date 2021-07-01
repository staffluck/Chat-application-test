from typing import List
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from .serializers import DialogSerializer, MessageSerializer
from .models import Dialog


class DialogListCreateView(ListCreateAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        return Dialog.objects.filter(users__id=self.request.user.id)


class MessagesDialogGetView(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        # return Dialog.objects.get(id=self.query_params)
        pass


def index(request):
    return render(request, 'chat/index.html')
