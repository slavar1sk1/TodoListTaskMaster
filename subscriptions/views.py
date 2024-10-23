# Import necessary modules and classes for views, forms, and user management
from django.views.generic import ListView, DetailView
from unicodedata import category
from user.models import TaskModel, UserProfile  # Models for tasks and user profiles
from user.forms import TaskModelForm  # Form for creating and editing tasks
from django.http import JsonResponse, HttpResponse  # To handle HTTP responses
from django.views.generic.edit import FormView, DeleteView, UpdateView  # For form handling and model updates
from django.contrib.auth.mixins import LoginRequiredMixin  # Ensures user is logged in
from .mixins import BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin  # Subscription mixins for access control
from django.shortcuts import render  # To render templates
from django.utils.decorators import method_decorator  # For applying decorators to class methods
from django.views.decorators.cache import never_cache  # Disables caching for specific views
from django.template.loader import render_to_string  # Renders templates as strings for dynamic content
from django.views.generic.base import View  # Basic view class

# View for displaying the list of tasks, restricted by subscription level
class TaskListView(LoginRequiredMixin, ListView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel  # The model we are listing (tasks)
    template_name = 'task_list.html'  # The template used for rendering
    context_object_name = 'tasks'  # The name of the list in the template context

    # Get the tasks for the logged-in user's profile
    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return TaskModel.objects.filter(user_profile=user_profile)

    # Add extra context to the template, including form and user-specific data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskModelForm()  # The task form for adding new tasks
        user_profile = self.request.user.userprofile
        context['rubies'] = user_profile.tasks_completed  # Show completed tasks (as rubies)
        context['status'] = user_profile.status  # Show user status (bronze, silver, gold)
        return context

    # Ensure the view is never cached
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# View for adding a new task, restricted by subscription level
class AddTaskView(LoginRequiredMixin, FormView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    form_class = TaskModelForm  # The form for adding a new task

    # Handle form submission
    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile  # Link the task to the user's profile
        task = form.save()

        if task:
            # Return task data as a JSON response for dynamic front-end updates
            return JsonResponse({
                'task': {
                    'id': task.id,
                    'task': task.task,
                    'status': task.status,
                    'category': task.category
                }
            })
        else:
            # Return an error response if task saving failed
            return JsonResponse({'error': 'Error saving task'}, status=500)

# View for deleting a task, restricted by subscription level
class DeleteTaskView(DeleteView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel  # The model to delete
    slug_field = 'id'  # The field used to identify the task
    slug_url_kwarg = 'task_id'  # The URL parameter for the task ID

    # Handle successful form submission
    def form_valid(self, form):
        self.object.delete()  # Delete the task

        # Reload the task list for the user's profile
        user_profile = self.request.user.userprofile
        html_task = render_to_string('task.html', {'tasks': TaskModel.objects.filter(user_profile=user_profile)}, self.request)

        return HttpResponse(html_task)  # Return the updated task list as HTML

# View for updating a task's status, restricted by subscription level
class UpdateTaskView(UpdateView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel  # The model to update
    slug_field = 'id'  # The field used to identify the task
    slug_url_kwarg = 'task_id'  # The URL parameter for the task ID
    fields = []  # No fields in the form, just updating the status

    # Handle form submission and update task status
    def form_valid(self, form):
        task = self.get_object()

        # If task is not completed, mark it as completed and update the user's profile
        if not task.status:
            task.status = True
            task.save()

            user_profile = task.user_profile
            user_profile.tasks_completed += 1  # Increment completed tasks
            user_profile.save()

        # Reload the task list and return the updated HTML with a custom header for the front-end
        user_profile = self.request.user.userprofile
        tasks = TaskModel.objects.filter(user_profile=user_profile)

        html_task_list = render_to_string('task.html', {'tasks': tasks}, self.request)
        response = HttpResponse(html_task_list)
        response.headers['HX-Trigger'] = 'updateRubins'  # Custom trigger for front-end updates

        return response

# Function to render tasks in the 'sport' category
def sport_category(request):
    user_profile = request.user.userprofile
    sport_category_tasks = TaskModel.objects.filter(category='sport', user_profile=user_profile)
    return render(request, 'sport_category.html', context={"sport_category_tasks": sport_category_tasks})

# Functions for rendering tasks in other categories (work, learning, leisure, etc.)
def other_category(request):
    user_profile = request.user.userprofile
    other_category_tasks = TaskModel.objects.filter(category='other', user_profile=user_profile)
    return render(request, 'other_category.html', context={"other_category_tasks": other_category_tasks})

def work_category(request):
    user_profile = request.user.userprofile
    work_category_tasks = TaskModel.objects.filter(category='work', user_profile=user_profile)
    return render(request, 'work_category.html', context={"work_category_tasks": work_category_tasks})

def learning_category(request):
    user_profile = request.user.userprofile
    learning_category_tasks = TaskModel.objects.filter(category='study', user_profile=user_profile)
    return render(request, 'learning_category.html', context={"learning_category_tasks": learning_category_tasks})

def leisure_category(request):
    user_profile = request.user.userprofile
    leisure_category_tasks = TaskModel.objects.filter(category='leisure', user_profile=user_profile)
    return render(request, 'leisure_category.html', context={"leisure_category_tasks": leisure_category_tasks})

# Function for rendering the subscription purchase page
def BuySubscriptions(request):
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()

    return render(request, 'buy_subscription.html', context={'status': user.status})

# Function to add rubies (points) to the user's profile
def add_rubins(request):
    user_profile = request.user.userprofile
    user_profile.tasks_completed += 100  # Add 100 rubies
    user_profile.status = 'bronze'  # Update status to bronze
    user_profile.save()
    return render(request, 'addrubins.html')

# AJAX view to update rubies count dynamically
class HxRubinsUpdate(View):
    def get(self, request, *args, **kwargs):
        tasks_completed = self.request.user.userprofile.tasks_completed
        return HttpResponse(str(tasks_completed))  # Return the number of completed tasks as plain text
