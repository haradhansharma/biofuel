from django.apps import AppConfig

class GlossaryConfig(AppConfig):
    """
    AppConfig for the 'glossary' app.

    This class defines configuration settings for the 'glossary' app.
    """

    # Specify the default auto field for this app's models.
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app. This should match the name of the app's directory.
    name = 'glossary'

    def ready(self):
        """
        Override the ready() method to import signals when the app is ready.

        This method is called when the application is loaded, and it provides
        an opportunity to perform initialization tasks. In this case, we are
        importing signals defined in the 'glossary.signals' module to ensure
        they are registered and ready to be used.
        """
        import glossary.signals
