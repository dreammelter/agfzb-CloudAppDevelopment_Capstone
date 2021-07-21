from django.apps import AppConfig


class DjangoappConfig(AppConfig):
    name = 'djangoapp'
    default_auto_field = 'django.db.models.AutoField' # turn off the BigAutoField warning