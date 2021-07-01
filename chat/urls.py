from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dialogs/', views.DialogListCreateView.as_view()),
    path('messages/<int:dialog_id>/', views.MessagesDialogGetView.as_view())
]
