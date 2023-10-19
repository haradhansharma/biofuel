---
title: Technical Guide Feedback app of GFVP
summary: Here given overview of the feedback app of Green fuel validation platform.
copyright: (c) gf-vp.com
repo_url: https://github.com/haradhansharma/biofuel
edit_uri: blob/v24123/gfvp_docs/docs
authors:
    - Haradhan Sharma
date: 2023-10-16

---

# Feedback App


This guide provides an overview of the Feedback app in GFVP, explaining its components and functionality.

## Admin Configuration (admin.py)

The `admin.py` file contains the Django Admin configuration for the Feedback Model. It defines how the Feedback model is displayed and filtered in the Django Admin interface. Here's an explanation of the key aspects:

```python

from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Feedback model.

    This class defines how the Feedback model should be displayed and
    filtered in the Django admin interface.

    Attributes:
        list_display (list of str): Fields to display in the list view.
        list_filter (tuple of str): Fields to use for filtering records.
        search_fields (tuple of str): Fields to use for searching records.
        ordering (tuple of str): Fields to determine the default ordering of records.
        readonly_fields (tuple of str): Fields that should be read-only in the admin interface.
    """

    # Display these fields in the list view of the admin interface.
    list_display = [f.name for f in Feedback._meta.fields if f.editable and not f.name == "id"]

    # Allow filtering by the 'url' field in the right sidebar.
    list_filter = ('url', )

    # Enable searching by 'message', 'name', and 'email' fields.
    search_fields = ('message', 'name', 'email', )

    # Order records by 'created_at' in descending order by default.
    ordering = ('-created_at',)

    # Make 'url', 'message', 'name', 'email', and 'phone' fields read-only.
    readonly_fields = ('url', 'message', 'name', 'email', 'phone',)
```


## Feedback App Forms

This module defines a Django form used for collecting and validating user feedback.

**FeedbackForm**

A Django form for the Feedback model. It includes fields for 'name', 'phone', 'email', 'url', and 'message', along with widget configurations for the form fields. The 'url' field is hidden and captures the URL from which feedback is submitted.

**Usage:**
- Import the form in your views.
- Use it to collect and validate user feedback data.
- Save the feedback instance to the database.

Example:

```python
from .forms import FeedbackForm

# Create an instance of the form
form = FeedbackForm(request.POST)

# Check if the form is valid
if form.is_valid():
    # Save the feedback instance
    feedback = form.save()
```

## Feedback App Models

`models.py` contains the Django model definition for storing user feedback.

**Feedback Model**

A Django model to represent user feedback. This model defines the structure and data fields for storing user feedback. It includes fields for 'name', 'phone', 'email', 'message', 'url', and 'created_at', along with the default ordering for feedback instances.

**Attributes:**
- `name` (models.CharField): The name of the person providing feedback.
- `phone` (models.CharField): The phone number of the person providing feedback.
- `email` (models.EmailField): The email address of the person providing feedback.
- `message` (models.TextField): The feedback message.
- `url` (models.URLField): The URL from which the feedback was submitted.
- `created_at` (models.DateTimeField): The timestamp when the feedback was created.

**Example Usage:**

```python
from .models import Feedback

# Create a new feedback instance
feedback = Feedback(name='John Doe', phone='123-456-7890', email='john@example.com', message='Great service!', url='http://example.com')

# Save the feedback instance to the database
feedback.save()
```
## Feedback App URL Configuration

`urls.py` defines the URL patterns and routing configuration for the Feedback app.

**App Namespace**

The app defines a namespace named `'feedback'` using `app_name`. This helps organize and group related URLs.

**URL Patterns:**
- `/submit/`: Handles the submission of user feedback.
- `/hx/`: Placeholder for additional URL patterns related to 'hx' (Hypertext) views.

**Example Usage:**

1. Submitting Feedback:
   - URL: `/submit/`
   - View: `submit_feedback`
   - Name: `'submit_feedback'`
   - Use this URL to access the feedback submission form.

2. Hypertext (hx) Views:
   - Additional URL patterns related to dynamic updates in web applications can be added here under the `/hx/` namespace.

```python
# Import the view for submitting feedback
from .views import submit_feedback
from django.urls import path

# Define the app namespace
app_name = 'feedback'

# Define URL patterns
urlpatterns = [
    # URL pattern for submitting feedback
    path('submit/', submit_feedback, name='submit_feedback'),
]

# Placeholder for additional 'hx' URL patterns
hx_urlpatterns = [
    # Add additional 'hx' URL patterns here if needed.
]

# Include 'hx' URL patterns in the main urlpatterns
urlpatterns += hx_urlpatterns
```

## Feedback App Views

`views.py` contains view functions for user feedback submissions in the Feedback app.

**submit_feedback View**

A view for handling user feedback submissions. It processes both GET and POST requests. When valid feedback data is submitted, it is saved, and the action is logged. For GET requests, the form is pre-filled with relevant data.

- URL: `/submit/`
- HTTP Method: POST for submission, GET for pre-filling.
- Handles form submission, data validation, and logging.
- Returns a success message on successful submission.

For more details, refer to the code in `views.py`.

## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.



## Credits

This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).
