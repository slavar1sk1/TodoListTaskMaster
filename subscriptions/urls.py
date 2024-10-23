# Import necessary modules
from django.urls import path  # Path function to define URL patterns
from .views import *  # Import all views from the current app

# Define the URL patterns for the task management app
urlpatterns = [
    # URL for the task list view
    path('task_list/', TaskListView.as_view(), name='task_list'),  # Displays a list of all tasks

    # URL for adding a new task
    path('add_task/', AddTaskView.as_view(), name='add_task'),  # Form view to add a task

    # URL for deleting a task (identified by its ID)
    path('delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),  # Deletes a specific task

    # URL for updating a task (identified by its ID)
    path('update/<int:task_id>/', UpdateTaskView.as_view(), name='update_task'),
    # Updates the status of a specific task

    # URL for purchasing a subscription
    path('buy_subscription', BuySubscriptions, name='buy_subscription'),  # Renders the subscription purchase page

    # URL for filtering tasks by the 'leisure' category
    path('leisure_category/', leisure_category, name='leisure_category'),  # Tasks filtered by 'leisure' category

    # URL for filtering tasks by the 'work' category
    path('work_category/', work_category, name='work_category'),  # Tasks filtered by 'work' category

    # URL for filtering tasks by the 'learning' category
    path('learning_category/', learning_category, name='learning_category'),  # Tasks filtered by 'learning' category

    # URL for filtering tasks by the 'other' category
    path('other_category/', other_category, name='other_category'),  # Tasks filtered by 'other' category

    # URL for filtering tasks by the 'sport' category
    path('sport_category', sport_category, name='sport_category'),  # Tasks filtered by 'sport' category

    # URL for adding rubies (points) to the user's profile
    path('addrubins/', add_rubins, name='addrubins'),  # Adds rubies to user profile

    # URL for dynamically updating rubies count via AJAX
    path('updaterubins/', HxRubinsUpdate.as_view(), name='updaterubins')
    # Updates rubies count with an HX-triggered event
]
