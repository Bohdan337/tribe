from django.apps import AppConfig

# The `SubjectConfig` class is used to configure the 'subject' application within the Django project.
class SubjectConfig(AppConfig):
    # Specifies the default auto field to be used for models in this app.
    default_auto_field = 'django.db.models.BigAutoField'
    # The name of the application, which is used for various Django configuration settings.
    name = 'subject'