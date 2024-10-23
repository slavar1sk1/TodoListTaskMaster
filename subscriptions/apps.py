# Importing the base AppConfig class from django.apps
from django.apps import AppConfig


# Configuration class for the 'subscriptions' app
class MyappConfig(AppConfig):
    # Specifies the type of auto-generated field for models that do not have a primary key field.
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of the app. This should match the folder name of your app.
    name = 'subscriptions'
