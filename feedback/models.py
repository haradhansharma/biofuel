from django.db import models

class Feedback(models.Model):
    """
    A Django model to represent user feedback.

    This model defines the structure and data fields for storing user feedback.
    It includes fields for 'name', 'phone', 'email', 'message', 'url', and
    'created_at', along with the default ordering for feedback instances.

    Attributes:
        name (models.CharField): The name of the person providing feedback.
        phone (models.CharField): The phone number of the person providing feedback.
        email (models.EmailField): The email address of the person providing feedback.
        message (models.TextField): The feedback message.
        url (models.URLField): The URL from which the feedback was submitted.
        created_at (models.DateTimeField): The timestamp when the feedback was created.
    """

    # Define the 'name' field for the user's name.
    name = models.CharField(max_length=100)
    
    # Define the 'phone' field for the user's phone number.
    phone = models.CharField(max_length=15)
    
    # Define the 'email' field for the user's email address.
    email = models.EmailField()
    
    # Define the 'message' field for the user's feedback message.
    message = models.TextField()
    
    # Define the 'url' field for the URL from which the feedback was submitted.
    url = models.URLField()
    
    # Define the 'created_at' field with auto_now_add set to True for automatic timestamping.
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Return a string representation of the feedback.

        This method is used to display a user-friendly representation of a
        feedback instance in the admin interface and other contexts.

        Returns:
            str: A string representation of the feedback, using the 'name' field.
        """
        return self.name
    
    class Meta:
        """
        Class to define the model's metadata, including ordering.

        This class specifies the default ordering of feedback instances based
        on the 'created_at' field in descending order.
        """
        ordering = ('-created_at',)    