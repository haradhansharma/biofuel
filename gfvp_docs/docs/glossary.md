---
title: Technical Guide Glossary App of GFVP
summary: Here given overview of the glossary app of Green fuel validation platform.
copyright: (c) gf-vp.com
repo_url: https://github.com/haradhansharma/biofuel
edit_uri: blob/v24123/gfvp_docs/docs
authors:
    - Haradhan Sharma
date: 2023-10-16

---

# Glossary App


## Introduction

The Glossary app is a Django application designed to manage and display glossary entries and user-submitted glossary requests within the Green Fuel Validation Platform project.

## Features

- Display a list of glossary entries.
- Allow users to submit glossary requests.
- Custom Django admin settings for managing glossary entries and requests.
- ...

## Installation

1. Clone the repository or download the project files.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Add 'glossary' to the `INSTALLED_APPS` list in your project's settings.
4. Run migrations to create the database tables: `python manage.py migrate`.


## Admin Configuration (admin.py)

In the `admin.py` file of the Glossary app, we configure the Django admin interface for managing glossary entries and requests. Here's an overview of what's done in this file:

```python
# Import necessary modules and classes from Django.
# ...

# Define an inline class for RelatedLinks to be used within the GlossaryAdmin.
# ...

# Define the admin class for the Glossary model.
class GlossaryAdmin(admin.ModelAdmin):
    """
    Custom admin settings for the Glossary model.
    """
    # Specify the model this admin class is associated with.
    # ...

    # Define the list of fields to be displayed in the admin list view.
    # ...

    # Define fields that can be searched in the admin list view.
    # ...

    # Include the RelatedLinksInline class as an inline form.
    # ...

# Register the GlossaryAdmin class with the Django admin site for the Glossary model.
admin.site.register(Glossary, GlossaryAdmin)

# Define the admin class for the GRequests model.
class GRequestsAdmin(admin.ModelAdmin):
    """
    Custom admin settings for the GRequests model.
    """
    # Specify the form to be used for this admin class.
    # ...

    # Specify the model this admin class is associated with.
    # ...

    # Define the list of fields to be displayed in the admin list view.
    # ...

# Register the GRequestsAdmin class with the Django admin site for the GRequests model.
admin.site.register(GRequests, GRequestsAdmin)
```


## AppConfig (app.py)

The `AppConfig` in the `app.py` file of the Glossary app provides configuration settings for the app within the Django project. Here's an overview of what's defined in this configuration:

```python
# Import necessary modules from Django.
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

```


## `forms.py` - Glossary App Forms

The `forms.py` file in the Glossary app defines the forms used for submitting and changing GRequests, including custom validation for certain fields.

### GRequestsChangeForm

The `GRequestsChangeForm` is used for changing GRequests model data. It includes custom validation for the 'description' field to ensure it is not empty.

```python
class GRequestsChangeForm(forms.ModelForm):
    """
    Form for changing GRequests model data.

    This form is used for changing the data of the GRequests model. It includes a custom
    validation for the 'description' field to ensure it is not empty.

    Attributes:
        Meta: A nested class defining metadata options for the form.
    """

    class Meta:
        model = GRequests
        fields = '__all__'

    def clean(self, *args, **kwargs):
        """
        Custom clean method for validating the 'description' field.

        This method checks if the 'description' field is empty and raises a
        forms.ValidationError if it is.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A cleaned data dictionary.
        """
        description = self.cleaned_data.get('description')

        if description == '':
            raise forms.ValidationError("Description Required")

        return super(GRequestsChangeForm, self).clean(*args, **kwargs)

```


## Glossary App Models

### Glossary

The `Glossary` model represents glossary entries in the system. It stores information about each entry, including its title, description, and automatically generated slug and anchor fields.

**Attributes:**

- `created` (DateTimeField): The date and time when the entry was created (auto-generated).
- `modified` (DateTimeField): The date and time when the entry was last modified (auto-generated).
- `title` (CharField): The title of the glossary entry.
- `slug` (SlugField): A unique slug based on the title (auto-generated).
- `anchor` (SlugField): A non-unique slug derived from the first character of the title (auto-generated).
- `description` (TextField): The description or definition of the glossary entry.

**Methods:**

- `__str__`: A string representation of the glossary entry, using its title.
- `save`: Custom save method to generate the slug and anchor fields based on the title.

**Meta:**

- `ordering` (list): Default ordering for glossary entries, first by title, then by modification date.

### RelatedLinks

The `RelatedLinks` model represents related links for glossary entries. It stores information about related links associated with glossary entries, including their title, URL link, and a foreign key reference to the related glossary entry.

**Attributes:**

- `title` (CharField): The title of the related link.
- `link` (URLField): The URL link.
- `glossary` (ForeignKey): A foreign key reference to the related glossary entry.

**Methods:**

- `__str__`: A string representation of the related link, including the associated glossary entry's title.

### GRequests

The `GRequests` model represents user-submitted requests for glossary entries. It stores information about G Requests, including their title and an optional description.

**Attributes:**

- `created` (DateTimeField): The date and time when the G Request was created (auto-generated).
- `modified` (DateTimeField): The date and time when the G Request was last modified (auto-generated).
- `title` (CharField): The title of the G Request.
- `description` (TextField, optional): Additional description or details of the request.

**Methods:**

- `__str__`: A string representation of the G Request, using its title.

**Meta:**

- `verbose_name` (str): The singular name for this model in the admin interface.
- `verbose_name_plural` (str): The plural name for this model in the admin interface.



## signals.py

In the `signals.py` file of the Glossary app, we define and configure signal receivers that respond to specific events in the application. In particular, we have a receiver function that gets triggered after a `GRequests` instance is saved. Here's an overview of what's done in this file:

```python
# Import necessary modules for working with Django signals.
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Import models and other dependencies from the current app.
from .models import *

# Import logging module for creating log entries.
import logging

# Get a logger instance named 'log'.
log = logging.getLogger('log')

# Define a receiver function to be triggered after saving a GRequests instance.
@receiver(post_save, sender=GRequests)
def make_glossary(sender, instance, created, *args, **kwargs):
    """
    Receiver function triggered after saving a GRequests instance.

    This function is a signal receiver that gets triggered after a GRequests
    instance is saved. It checks if the instance is newly created (created=True),
    and if not, it creates a Glossary entry based on the GRequests instance and
    then deletes the GRequests instance.

    Args:
        sender: The sender of the signal.
        instance: The instance of the GRequests model.
        created (bool): Indicates whether the GRequests instance was newly created.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """
    if created:
        # If the GRequests instance is newly created, do nothing.
        pass   
    else: 
        # If the GRequests instance is not newly created, create a Glossary entry.
        log.info('Glossary created from request________________')   
        Glossary.objects.create(title = instance.title, description = instance.description)
        
        # Delete the GRequests instance since it's now been converted to a Glossary entry.
        instance.delete()     
```



## URL Configuration (urls.py)

In the `urls.py` file of the Glossary app, we define the URL patterns for accessing the app's views. Here's an overview of the URL configuration:

```python
# Import necessary modules and views from the Glossary app.
# ...

# Define the app name for URL namespace.
app_name = 'glossary'

# Define URL patterns for the 'glossary' app.
urlpatterns = [
    # Define a URL pattern for the glossary list view.
    path('', views.Glist.as_view(), name='g_list'),    
]
```

## Views (views.py)

In the `views.py` file of the Glossary app, we define view functions and classes responsible for rendering glossary-related web pages, handling user requests, and providing additional context data. Here's an overview of the views and their functionality:

### Glist (Class-based View)

The `Glist` class-based view is responsible for displaying the glossary list, handling glossary request submissions, and providing additional context data. Here's a breakdown of its attributes and methods:

**Attributes:**

- `model (Glossary)`: The model to query for glossary entries.
- `paginate_by (int, optional)`: Uncomment to enable pagination with a specific number of entries per page.

**Methods:**

- `get_context_data(**kwargs)`: Overrides the base class method to provide additional context data for rendering the glossary list view. It includes a form for submitting glossary requests and meta information.

- `post(request, *args, **kwargs)`: Handles POST requests for submitting glossary requests. It validates the request form, saves the request if it's valid, and provides feedback to the user via messages.

The `Glist` view plays a crucial role in managing glossary entries and user interactions with the glossary section of the application.

By using this view, users can view glossary entries, submit requests for new glossary entries, and receive feedback on their submissions.

This view also incorporates meta information for SEO purposes, enhancing the user experience.

Keep in mind that pagination can be enabled by uncommenting the `paginate_by` attribute and specifying the desired number of entries per page.

## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.


## Credits

This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).