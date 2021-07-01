from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from .serializers import DialogSerializer
from .models import Dialog


class DialogListCreateView(ListCreateAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        return Dialog.objects.filter(users__in=self.request.user)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })