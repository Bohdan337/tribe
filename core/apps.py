from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    The `CoreConfig` class is used to configure the 'core' application within the Django project.
    """
    # Specifies the default auto field to be used for models in this app.
    default_auto_field = 'django.db.models.BigAutoField'
    # The name of the application, which is used for various Django configuration settings.
    name = 'core'