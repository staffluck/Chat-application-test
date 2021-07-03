from typing import List
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import DialogSerializer, MessageSerializer
from .models import Dialog


class MessagesPagination(PageNumberPagination):
    page_size = 10


class DialogListCreateView(ListCreateAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        return Dialog.objects.filter(users__id=self.request.user.id)


class MessagesDialogListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    pagination_class = MessagesPagination

    def get_queryset(self):
        dialog_id = self.request.path.split('/')[-2]
        dialog = Dialog.objects.filter(id=dialog_id)
        if dialog.exists():
            return dialog.first().messages.all()
        return []


def index(request):
    return render(request, 'chat/index.html')
