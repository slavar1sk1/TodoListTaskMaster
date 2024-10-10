"""Create Forms for Authentication"""

from django import forms
from .models import User, TaskModel, UserProfile, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create Authentication Form
class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'username'})
            self.fields['password1'].widget.attrs.update({'class': 'password'})


# Create Registration Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs.update({'class': 'email'})
            self.fields['username'].widget.attrs.update({'class': 'username'})
            self.fields['password1'].widget.attrs.update({'class': 'password1'})
            self.fields['password2'].widget.attrs.update({'class': 'password2'})


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['task', 'category']
        widgets = {
            'category': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = TaskModel.CATEGORY_CHOICES

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            instance.user_profile = user_profile
        if commit:
            instance.save()
        return instance