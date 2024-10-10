from lib2to3.fixes.fix_input import context

from django.views.generic import ListView
from unicodedata import category

from user.models import TaskModel, UserProfile
from user.forms import TaskModelForm
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string


class TaskListView(LoginRequiredMixin, ListView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return TaskModel.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskModelForm()
        user_profile = self.request.user.userprofile
        context['rubies'] = user_profile.tasks_completed
        context['status'] = user_profile.status
        return context
    
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AddTaskView(LoginRequiredMixin, FormView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    form_class = TaskModelForm

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile
        task = form.save()
        
        if task:
            return JsonResponse({
                'task': {
                    'id': task.id,
                    'task': task.task,
                    'status': task.status,
                    'category': task.category
                }
            })
        else:
            return JsonResponse({'error': 'Ошибка при сохранении задачи'}, status=500)


class DeleteTaskView(DeleteView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel
    slug_field = 'id'
    slug_url_kwarg = 'task_id'

    def form_valid(self, form):
        self.object.delete()

        user_profile = self.request.user.userprofile
        html_task = render_to_string('task.html', {'tasks': TaskModel.objects.filter(user_profile=user_profile)}, self.request)

        return HttpResponse(html_task)


class UpdateTaskView(UpdateView, BronzeSubscriptionRequiredMixin, SilverSubscriptionRequiredMixin, GoldSubscriptionRequiredMixin):
    model = TaskModel
    slug_field = 'id'
    slug_url_kwarg = 'task_id'

    fields = []

    def form_valid(self, form):
        task = self.get_object()

        if not task.status:
            task.status = True
            task.save()

            user_profile = task.user_profile
            user_profile.tasks_completed += 1
            user_profile.save()

        user_profile = self.request.user.userprofile
        tasks = TaskModel.objects.filter(user_profile=user_profile)
        rubies = user_profile.tasks_completed

        html_task_list = render_to_string('task.html', {'tasks': tasks}, self.request)
        html_rubies = f'<span id="rubies-count">{rubies}</span>'

        return HttpResponse(f"{html_task_list}||{html_rubies}")


def sport_category(request):
    user_profile = request.user.userprofile
    sport_category_tasks = TaskModel.objects.filter(category='sport', user_profile=user_profile)
    return render(request, 'sport_category.html', context={"sport_category_tasks":sport_category_tasks})


def other_category(request):
    user_profile = request.user.userprofile
    other_category_tasks = TaskModel.objects.filter(category='other', user_profile=user_profile)
    return render(request, 'other_category.html', context={"other_category_tasks":other_category_tasks})


def work_category(request):
    user_profile = request.user.userprofile
    work_category_tasks = TaskModel.objects.filter(category='work', user_profile=user_profile)
    return render(request, 'work_category.html', context={"work_category_tasks":work_category_tasks})


def learning_category(request):
    user_profile = request.user.userprofile
    learning_category_tasks = TaskModel.objects.filter(category='study', user_profile=user_profile)
    return render(request, 'learning_category.html', context={"learning_category_tasks":learning_category_tasks})

def leisure_category(request):
    user_profile = request.user.userprofile
    leisure_category_tasks = TaskModel.objects.filter(category='leisure', user_profile=user_profile)
    return render(request, 'leisure_category.html', context={"leisure_category_tasks":leisure_category_tasks})


def BuySubscriptions(request):
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()

    return render(request, 'buy_subscription.html',
                  context={'status': user.status})


def add_rubins(request):
    user_profile = request.user.userprofile
    user_profile.tasks_completed += 100
    user_profile.status = 'bronze'
    user_profile.save()
    return render(request, 'addrubins.html')
