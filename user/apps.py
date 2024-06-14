from django.apps import AppConfig


# The `UserConfig` class in Python sets the default auto field to `BigAutoField` for the `user` app.
class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
