from tkinter.font import names

from django.urls import path
from .views import *


urlpatterns = [
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('add_task/', AddTaskView.as_view(), name='add_task'),
    path('delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),
    path('update/<int:task_id>/', UpdateTaskView.as_view(), name='update_task'),
    path('buy_subscription', BuySubscriptions, name='buy_subscription'),
    path('leisure_category/', leisure_category, name='leisure_category'),
    path('work_category/', work_category, name='work_category'),
    path('learning_category/', learning_category, name='learning_category'),
    path('other_category/', other_category, name='other_category'),
    path('sport_category', sport_category, name='sport_category'),
    path('addrubins/', add_rubins, name='addrubins')]
