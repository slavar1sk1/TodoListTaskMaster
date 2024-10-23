"""Create Forms for Authentication"""

from django import forms
from .models import User, TaskModel, UserProfile, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create Authentication Form
class LoginForm(AuthenticationForm):
    # Customize the password field to use a password input widget for security.
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  # Specify the model for this form.
        fields = ['username', 'password']  # Fields to include in the form.

    # Customizing the initialization method to add CSS classes to form fields.
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)  # Call the parent class's constructor.
        self.fields['username'].widget.attrs.update({'class': 'username'})  # Add class for styling.
        self.fields['password'].widget.attrs.update({'class': 'password'})  # Add class for styling.


# Create Registration Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Specify the model for this form.
        fields = ['email', 'username', 'password1', 'password2']  # Fields to include in the form.

    # Customizing the initialization method to add CSS classes to form fields.
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)  # Call the parent class's constructor.
        self.fields['email'].widget.attrs.update({'class': 'email'})  # Add class for styling.
        self.fields['username'].widget.attrs.update({'class': 'username'})  # Add class for styling.
        self.fields['password1'].widget.attrs.update({'class': 'password1'})  # Add class for styling.
        self.fields['password2'].widget.attrs.update({'class': 'password2'})  # Add class for styling.


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel  # Specify the model for this form.
        fields = ['task', 'category']  # Fields to include in the form.
        widgets = {
            'category': forms.Select()  # Use a dropdown for category selection.
        }

    # Customizing the initialization method to set category choices.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent class's constructor.
        self.fields['category'].choices = TaskModel.CATEGORY_CHOICES  # Set available category choices.

    # Overriding the save method to associate the task with the user's profile.
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)  # Create the instance but don't save it yet.
        if user:
            user_profile, created = UserProfile.objects.get_or_create(user=user)  # Get or create the user's profile.
            instance.user_profile = user_profile  # Link the task to the user's profile.
        if commit:
            instance.save()  # Save the instance if requested.
        return instance  # Return the saved instance.
