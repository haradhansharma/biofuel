from django.apps import AppConfig


class EvaluationConfig(AppConfig):
    """
    AppConfig for the 'evaluation' app.

    This AppConfig class provides configuration settings for the 'evaluation' app.

    Attributes:
        default_auto_field (str): The name of the default auto-generated primary key field.
        name (str): The name of the app.

    Methods:
        ready(): This method is executed when the app is ready. It imports the signals module for the app.

    Example:
        To use this AppConfig in your Django project, add it to the 'INSTALLED_APPS' list in your project's
        settings.py file as follows:

        INSTALLED_APPS = [
            ...
            'evaluation',
            ...
        ]
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evaluation'
    
    def ready(self):
        """
        This method is executed when the app is ready.

        It imports the signals module for the app. Signals are used to perform certain actions when certain events
        occur within the app, such as when database records are created or updated.

        Example:
            The 'import evaluation.signals' statement in this method ensures that the signals defined in the
            'signals.py' module of the 'evaluation' app are loaded and can be used to handle specific events within
            the app.

        Signals are a powerful tool in Django for decoupling various parts of an application, and they allow
        developers to respond to changes in the system without directly coupling components together.

        Returns:
            None
        """
        import evaluation.signals
