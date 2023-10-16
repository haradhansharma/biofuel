Custom Django Admin Configuration for Accounts App
==================================================

This apps contains a custom Django admin configuration for managing user accounts and related models in an application. The admin configuration enhances the default Django admin interface by adding custom actions, custom fields, and filtering options.


Overview
--------

The provided code extends the Django admin interface to manage user accounts, user profiles, and other related models. It includes custom actions for activating and deactivating user accounts, as well as sending emails to specific user groups. The customizations are designed to provide a more efficient way of managing users within the Django admin dashboard.

Setup
-----

To use this custom admin configuration in your Django project, follow these steps:

1. Copy the provided code to your Django project's admin.py file or a dedicated admin.py file within your app.
2. Make sure you have the required models, forms, and templates as referenced in the code.
3. Register the required models using the `admin.site.register()` function.
4. Customize the custom actions, filters, and other admin settings to match your project's requirements.
5. Run your Django development server and navigate to the admin dashboard to see the changes.

Features
--------

- Customized user list view with additional fields such as user type, expertise, phone number, and email verification status.
- Filtering users based on user type, activity status, staff status, expertise, and email verification status.
- Searching for users based on email, phone, organization, username, expertise, and email verification status.
- Inline editing of user profiles within the user admin page.
- Ordering users by their date of joining.
- Custom actions for activating and deactivating user accounts.
- Custom action for sending emails to selected marine experts for feedback updates.
- Management of user types with customizable display fields and filtering options.

Custom Actions
--------------

### Activate Account and Send Mail

This action allows admin users to activate selected user accounts and send activation emails to the users. Admins can select multiple users and trigger the action to activate their accounts.

### Deactivate Account

This action enables admin users to deactivate selected user accounts. Similar to the previous action, admin users can select multiple users and deactivate their accounts.

### Send Mail to Expert

Admin users can use this action to send courtesy emails to selected marine experts for feedback updates. The action is restricted to marine experts only. An email template is used for composing the emails.

UserType Management
-------------------

The custom admin configuration also provides enhanced management for user types:

- Displaying user type fields in the admin list view.
- Filtering user types based on their names.
- Searching for user types using their names.
- Automatically populating the `slug` field based on the `name` field.


Optimized Django User Type Decorators
=====================================

Overview
--------

This repository provides optimized decorators for controlling access to Django views based on user types, as well as a decorator for report creator access control. These decorators simplify the process of restricting access to specific user types or report creators, enhancing the security and usability of your Django application.

Installation
------------

1. Copy the provided optimized decorators code to a suitable location within your Django project, such as a utility module.
2. Import the decorators wherever you need to control access based on user types or report creator permissions.

Usage
-----

1. Import the required decorators in your views or viewsets:

   .. code-block:: python

      from your_project.utils.decorators import expert_required, producer_required, consumer_required, marine_required, report_creator_required

2. Apply the decorators to your views or viewsets where access control is needed:

   .. code-block:: python

      @expert_required
      def expert_view(request, ...):
          # Your view logic here
          ...

      @report_creator_required
      def report_edit_view(request, slug, ...):
          # Your view logic here
          ...

User Type Decorators
---------------------

The following user type decorators are available:

- ``expert_required``: Requires the user to be an expert, staff member, or superuser.
- ``producer_required``: Requires the user to be a producer, staff member, or superuser.
- ``consumer_required``: Requires the user to be a consumer, staff member, or superuser.
- ``marine_required``: Requires the user to be a marine user, staff member, or superuser.

Report Creator Decorator
------------------------

The ``report_creator_required`` decorator restricts access to views based on the report creator or staff/superuser. This is particularly useful for views related to report editing or management.



Custom UserCreationForm for Admin
=================================

The `UserCreationForm` class provided in this app is a customized version of Django's default `UserCreationForm`. It extends the functionality of the default form to include additional fields and customization options.

Usage
-----

The `UserCreationForm` can be used for creating new user accounts with extended fields. It adds the following features:

- Additional fields: The form includes custom fields such as `usertype`, `experts_in`, and `term_agree`.
- Customized appearance: The form's appearance on the admin page is customized using the `UserAdmin.add_fieldsets` attribute.
- Compatibility with UserAdmin: The form is compatible with the Django `UserAdmin` interface.

Customization
-------------

The `UserCreationForm` is designed to enhance the default user registration process. It inherits from Django's `UserCreationForm` and extends its functionality:

- The `__init__` method initializes the form instance.
- The `UserAdmin.add_form` is set to use the Django's default `UserCreationForm`.
- The `UserAdmin.add_fieldsets` are updated to include the additional fields and customize the appearance.

To use this form in your project, simply import it and use it for user registration with the extended fields.

.. code-block:: python

    from django.contrib.auth.forms import UserCreationForm as UserCreationFormDjango
    from .forms import UserCreationForm  # Import the custom form
    from django.contrib.auth.admin import UserAdmin

    # Set the UserAdmin's add_form to use the custom UserCreationForm
    UserAdmin.add_form = UserCreationFormDjango


UserCreationFormFront for user registration
===========================================

The `UserCreationFormFront` class is a custom user creation form specifically designed for the frontend registration page of your Django project's account app. This form extends the `UserCreationFormDjango` class.

Usage
-----

This form includes various custom fields with HTML attributes to enhance user experience during registration. It also implements validations for username, email, and other fields. Additionally, it integrates with Google reCAPTCHA for added security.

Custom Fields
-------------

- `username`: A field for the username with a placeholder and real-time username availability check using AJAX.
- `email`: An email field with a placeholder and real-time email availability check using AJAX.
- `password1`: A password field for the user's password.
- `password2`: A field to confirm the password.
- `term_agree`: A checkbox for agreeing to terms and conditions.
- `newsletter_subscription`: A checkbox to subscribe to the newsletter.

Custom Widgets
--------------

The form uses various custom widgets for improved user interactions:

- `usertype`: A dropdown widget for selecting the user type with AJAX-based data loading.
- `experts_in`: A dropdown widget for selecting areas of expertise.
- `orgonization`: A text input widget for the user's organization.
- `is_public`: A checkbox widget for specifying whether the user's profile is public.

Validation and Email Verification
----------------------------------

The `UserCreationFormFront` class contains methods for custom field validation:

- `clean_username()`: Validates the username to disallow spaces.
- `clean_experts_in()`: Validates the `experts_in` field based on the user type.
- `clean()`: Implements a custom clean method for handling various validations and email verifications during registration.

Email Verification Flow
------------------------

The form handles email verification during registration:

- If the provided email is not registered, the user can proceed with registration.
- If the email is already registered but not verified, a verification email is sent to the user for confirmation.
- If the email is verified but the account is not activated, the user receives a courtesy email and a message regarding activation status.

Please note that this README provides a summary of the `UserCreationFormFront` class and its functionalities. For detailed implementation and integration instructions, refer to the associated source code and documentation within your Django project's `account` app.


Custom UserChangeForm for Self-Account Data Editing
===================================================

Introduction
------------

The `UserChangeForm` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `UserChangeForm` class provided in this module is a custom form derived from Django's `UserChangeForm`. Its purpose is to extend the functionality of the default form to allow users to edit their own account data. This form is primarily used within the settings and password change sections of the dashboard.

Usage
-----

To make use of the `UserChangeForm`, adhere to the following steps:

1. Import the form into your views or forms module:

   .. code-block:: python

       from path.to.UserChangeForm import UserChangeForm

2. In your view or form class, create an instance of the `UserChangeForm`:

   .. code-block:: python

       user_change_form = UserChangeForm(instance=request.user)

3. Render the form within your template:

   .. code-block:: html

       <form method="post">
           {% csrf_token %}
           {{ user_change_form.as_p }}
           <button type="submit">Save Changes</button>
       </form>

Fields and Widgets
-------------------

The `UserChangeForm` inherits the fields and widgets of the default `UserChangeForm` provided by Django. However, this implementation extends these fields with additional customization, specifically:

- **Email:** The email field is tailored to use the `forms.EmailInput` widget. This results in an email input field that has the `form-control` class and an `aria-label` attribute, thereby enhancing accessibility.

   .. code-block:: python

       widgets = {
           'email': forms.EmailInput(attrs={'class': 'form-control', 'aria-label': 'email'}),
       }

Meta Class
----------

The `Meta` class within the `UserChangeForm` specifies the model to be utilized and the fields to be included in the form. In this case, the form is configured to operate with the user model returned by `get_user_model()` and encompasses all fields.

   .. code-block:: python

       class Meta:
           model = get_user_model()
           fields = '__all__'





`LoginForm` Class in Account App
================================

Overview
--------

The `LoginForm` class is a custom login form designed for the Django project's `account` app. This form extends the default `AuthenticationForm` provided by Django, adding additional fields, custom validations, and integrating reCAPTCHA for enhanced security.

Features
--------

- **Customized Fields:** The `LoginForm` customizes the default Django form fields, adding HTML attributes to improve user experience. The `username` and `password` fields are styled using the `form-control` CSS class.

- **Remember Me Option:** A "Remember Me" checkbox allows users to choose whether to remember their login for 30 days, as per the site settings. This feature enhances user convenience.

- **reCAPTCHA Integration:** The form includes a Google reCAPTCHA field to prevent automated bot submissions. The reCAPTCHA is displayed as a checkbox for user interaction.

Additional Details
------------------

- **Meta Class:** The `Meta` class within the `LoginForm` specifies the model and fields used in the form. The fields included in the form are `username`, `password`, and `remember_me`.

- **Custom Validation:** The `clean` method of the `LoginForm` class implements custom validation and checks. It ensures that the reCAPTCHA is completed and verifies the provided email and password.

  - If the reCAPTCHA is not completed, a validation error is raised, requiring the user to complete the CAPTCHA.

  - If the provided email and password are valid, the form checks if the email exists in the system. If the email does not exist, an error message is displayed.

  - If the email exists but is not verified, the user is sent an email verification link for verification. A warning message is also displayed to the user.

  - If the email is verified but not activated, different actions are taken based on the user's type (expert, marine, etc.). For certain user types, the user is notified that their account is awaiting approval. For others, an activation email is resent.

  - If the email is verified and activated, the user is authenticated using their email and password. If the authentication fails, an error message is shown.

Usage
-----

To utilize the `LoginForm` class, follow these steps:

1. Import the `LoginForm` class into the appropriate module:

    .. code-block:: python

      from account.forms import LoginForm
    

2. Use the `LoginForm` class in your views, passing it to your template context for rendering:

    .. code-block:: python

       def login_view(request):
           # ...
           form = LoginForm(request, ...)
           # ...
   

3. Render the form in your template using Django template tags:

    .. code-block:: html

       <form method="post">
           {% csrf_token %}
           {{ form.as_p }}
           <button type="submit">Login</button>
       </form>
    

Notes
-----

- Ensure that the necessary Django imports and configurations are set up before using the `LoginForm` class.

- Modify the form template as needed to match your project's styling and design.

- The form relies on reCAPTCHA. Make sure to set up reCAPTCHA keys in your project settings for the CAPTCHA field to function properly.

For further assistance or customization, refer to the Django documentation and comments within the code.



Helper of Accounts APP
======================

This is a brief description of the My App project.

Custom Username Validator
-------------------------

.. code-block:: python

    class CustomsernameValidator(UnicodeUsernameValidator, ASCIIUsernameValidator):
        """
        Custom username validator that allows only letters, numbers, and periods.
        """

        ...

Permission Check Function
-------------------------

The following function is abandoned and not currently in use:

.. code-block:: python

    def check_type(request, slug):
        """
        Checks if the current user has the permission to access the requested resource.

        Args:
            request (django.http.HttpRequest): The HTTP request object.
            slug (str): The slug of the user type.

        Raises:
            PermissionDenied: If the current user does not have the permission to access the requested resource.
        """

        ...

Email Function
--------------

The following function sends an email to all admins:

.. code-block:: python

    def send_admin_mail(subject, message):
        """
        Sends an email to all admins.

        Args:
            subject (str): The email subject.
            message (str): The email message.
        """

        ...


Automatic Profile Creation
==========================

The `accounts` app includes a signal that automatically creates or updates user profiles whenever a new user is registered or an existing user is saved. This functionality is achieved through the use of Django signals.

Whenever a `User` instance is created, the signal is triggered, and the `create_or_update_user_profile` function is called. This function checks if the user is newly created or being updated and accordingly creates a new profile or updates the existing one.

Usage
-----

To use this automatic profile creation feature in your Django project, follow these steps:

1. Make sure the `accounts` app is installed in your project and properly configured.

2. In your `accounts` app, create a file named `signals.py` if it doesn't already exist.

3. Add the following code to your `signals.py` file:

.. code-block:: python    

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        ...

4. In the above code, make sure to replace `'models'` with the correct import path to your `Profile` model if it's in a different module or app.

5. In your project's `settings.py` file, add the `'accounts.signals'` module to the `INSTALLED_APPS` list to ensure that the signal is properly connected.

6. You can uncomment the `post_save.connect(create_or_update_user_profile, sender=User)` line in the `signals.py` file or connect the signal in your preferred way.

With these steps completed, your project will automatically create or update user profiles whenever a new user is registered or an existing user is saved.

Remember to run your project's migrations after making these changes to ensure that the database schema is updated accordingly.


Automatic Notification Settings Creation
========================================

The `accounts` app includes a signal that automatically creates or updates notification settings associated with a user whenever a new user is registered or an existing user is saved. This functionality is achieved through the use of Django signals.

Whenever a `User` instance is created or updated, the signal is triggered, and the `create_or_update_notification_settings` function is called. This function checks if the user is newly created or being updated and accordingly creates a new notification setting or updates the existing one.

Usage
-----

To use this automatic notification settings creation feature in your Django project, follow these steps:

1. Make sure the `accounts` app is installed in your project and properly configured.

2. In your `accounts` app, create a file named `signals.py` if it doesn't already exist.

3. Add the following code to your `signals.py` file:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, NotificationSettings

@receiver(post_save, sender=User)
def create_or_update_notification_settings(sender, instance, created, **kwargs):
    """
    Creates or updates a notification setting associated with the User model.
    As it has been created after an existing user, we are checking for creating notification if it doesn't exist to avoid errors.

    Args:
        sender (Model): The model class that sent the signal (User in this case).
        instance (User): The specific instance of the User model that was saved.
        created (bool): Indicates whether a new instance was created or an existing one was saved.
        **kwargs: Additional keyword arguments passed along with the signal.

    Returns:
        None
    """
    try:
        notification_settings = instance.notificationsettings  # Attempt to access the related NotificationSettings
    except NotificationSettings.DoesNotExist:
        notification_settings = None

    if created or notification_settings is None:
        # Create a notification settings or update the existing one
        notification_settings, created = NotificationSettings.objects.get_or_create(user=instance)

    # Now, make sure that the instance.notificationsettings is set properly
    if instance.pk != notification_settings.pk:
        instance.notificationsettings = notification_settings
        instance.save()






Account Activation Token Generator
==================================

Accounts app includes a custom token generator, `AccountActivationTokenGenerator`, which is used to generate tokens for email validation during user signup. This token generator extends Django's built-in `PasswordResetTokenGenerator` to add activation-related information.

Usage
-----

To use the `AccountActivationTokenGenerator` for email validation during user signup, follow these steps:

1. Make sure the `accounts` app is installed in your project and properly configured.

2. In your project's `settings.py` file, ensure that the `'accounts'` app is included in the `INSTALLED_APPS` list.

3. In your `accounts` app, create a file named `tokens.py` if it doesn't already exist.

4. Add the following code to your `tokens.py` file:

.. code-block:: python    

    class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
        def _make_hash_value(self, user, timestamp):
            ...

    account_activation_token = AccountActivationTokenGenerator()

5. In the above code, `AccountActivationTokenGenerator` extends Django's `PasswordResetTokenGenerator` and includes custom logic for generating tokens with user activation information.

6. The `account_activation_token` instance of the `AccountActivationTokenGenerator` class can be used to generate tokens for user email validation during signup.


URL Configuration
=================

Here's an overview of the URL patterns defined in the `urls.py` file of the `accounts` app:

1. User Signup:
    URL: `/signup/`
    View: `views.signup`
    Description: The endpoint for user registration. Renders the signup form and handles form submission.

2. User Login:
    URL: `/login/`
    View: `views.CustomLoginView`
    Description: The endpoint for user login. Uses a custom login view to manage authentication and redirection.

3. User Profile:
    URL: `/my-profile/`
    View: `views.userpage`
    Description: The endpoint for the user's profile page. Displays the user's profile information and related details.

4. User Activation:
    URL: `/activate/<uidb64>/<token>/`
    View: `views.activate`
    Description: The endpoint for user account activation via token. Activates a user's account using the provided token.

5. Check Username Availability:
    URL: `/check-username/`
    View: `views.check_username`
    Description: Endpoint to check the availability of a chosen username during registration.

6. Check Email Availability:
    URL: `/check-email/`
    View: `views.check_email`
    Description: Endpoint to check the availability of a chosen email address during registration.

7. Commit User Service:
    URL: `/<str:user_id>/<str:na_id>/commit-service/`
    View: `views.commit_service`
    Description: Endpoint to commit a service associated with a user's profile.

8. Delete User Service:
    URL: `/<str:user_id>/<str:na_id>/delete-service/`
    View: `views.delete_service`
    Description: Endpoint to delete a service associated with a user's profile.





Custom Login View
=================

.. note::
   This section describes the custom login view implemented in this project.

    The project includes a custom login view called ``CustomLoginView``, which is built upon Django's built-in ``LoginView`` class. This custom view allows for fine-grained control over the login process and introduces additional features.

Features
--------

   - Uses a custom login form (``LoginForm``) to collect user credentials.
   - Sets a custom URL for redirection after a successful login.
   - Handles the 'remember me' functionality to control session duration.

Usage
-----

To use the custom login view in your project, follow these steps:

1. Ensure that you have the necessary prerequisites and Django set up.
2. Copy the ``CustomLoginView`` class from the provided source code.
3. Import the necessary modules and classes in your project, including the custom form (``LoginForm``).

Example Usage
-------------

Below is an example of how you might use the ``CustomLoginView`` in your Django project's ``views.py``:

.. code-block:: python

    from django.urls import reverse_lazy
    from custom_login_app.forms import LoginForm  # Import the custom LoginForm
    from custom_login_app.views import CustomLoginView  # Import the CustomLoginView

    class MyCustomLoginView(CustomLoginView):
        form_class = LoginForm  # Use the custom LoginForm
        next_page = reverse_lazy('accounts:user_link')  # Set a custom redirection URL

Context Data
------------

The custom login view also provides additional context data to enhance the rendering of the login page. This includes meta information such as title, description, tags, and robots.



Signup View
===========

The `signup` view function is responsible for handling user signup and registration. It provides a user-friendly interface for users to create accounts on the website. The view supports various user types and expert subtypes.

.. code-block:: python

    def signup(request):
        """
        View function for user signup.
        
        This view handles the signup procedure for different user types and experts' subtypes.
        The process involves segregating users based on their selected user type or expert subtype.
        Users who have already selected a user type during their session are directed to the signup form.
        If anyone attempts to signup without selecting a user type, they are redirected to choose one.
        Expert users only need to select the "Expert" user type during signup.
        
        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: The rendered signup page or redirection to appropriate pages.
        :rtype: HttpResponse
        """

Features
--------

- User Type Segregation: Users are directed to select their user type or expert subtype before proceeding with registration. This segregation ensures accurate registration and user role assignment.

- Email Confirmation: After submitting the signup form, users receive an email confirmation containing an activation link. This link is used to verify the user's email address and complete the registration process.

- Interactive Frontend: The frontend of the signup page is interactive, guiding users through the registration process. The form is pre-filled with default values, ensuring a seamless user experience.

Installation
------------

1. Install the required Python packages using pip:

   .. code-block:: bash

       pip install -r requirements.txt

2. Add the `account` app to your Django project's settings:

   .. code-block:: python

       INSTALLED_APPS = [
           # ...
           'account',
           # ...
       ]

3. Include the app's URLs in your project's URL configuration:

   .. code-block:: python

       from django.urls import path
       from account.views import signup

       urlpatterns = [
           # ...
           path('signup/', signup, name='signup'),
           # ...
       ]





Activate User Account
=====================

The `accounts` app provides functionality for user account activation and related actions after the signup process.


The `activate` function in this app is responsible for activating a user's account using the provided activation link. The following actions are performed during the activation process:

1. Preparation of data for the site.
2. Verification of the activation URL and decoding of the user ID.
3. If the activation link is valid, the user's account is marked as email verified.

    a. If the user is an expert or marine, the account is activated manually by the site admin, and the user is notified to wait for approval.
    b. If the user is not an expert, the account is activated automatically, and an account activation email is sent.

4. User data is saved, considering different approval policies based on user type.

Creating Lead
-------------

After the activation process, the app performs the following actions:

1. Retrieves location information from the HTTP request.
2. Creates a lead using the user's full name, email address, city, and country information.

Creating Newsletter Subscription
--------------------------------

The app also handles newsletter subscriptions:

1. If the user has opted to receive the newsletter during signup, the app checks whether the user's email already exists in the CRM.
2. If the email exists, the subscription status is updated to `True`.
3. If the email does not exist, a new lead is created with the user's information, and the subscription status is set to `True`.

Usage
-----

To use the `activate` function, pass the required arguments:

- `request` (HttpRequest): The HTTP request object.
- `uidb64` (str): The base64-encoded user ID.
- `token` (str): The activation token.

The function will redirect to appropriate views based on the activation result.

Make sure to configure your project's URLs and templates accordingly to handle the activation process and related notifications.

Note: This readme provides a summary of the `activate` function's functionality. Please refer to the source code for complete implementation details.


User Profile Page View
======================

This Django view function displays a user's profile page, providing information about their reports and activities.

Usage
-----

1. Decorator Usage:
    This view function is decorated with `@login_required` to ensure that only authenticated users can access it.

2. Input:
    - `request` (HttpRequest): The HTTP request object sent by the client.

3. Output:
    - `HttpResponse`: The rendered user profile page with relevant user data.

Functionality
-------------

- When a user accesses their profile page, the following steps are performed:

  1. Clear the session data to ensure a clean state when the user logs in.

  2. Retrieve the user from the request.

  3. Check if a report slug is provided in the query parameters. If so, attempt to retrieve the corresponding report.

  4. If no report slug is provided, retrieve the most recent report created by the user.

  5. If a report is found, generate label-wise data from the report.

  6. Calculate statistics based on the label data:
     - `ans_ques`: Total answered questions
     - `dont_know_ans`: Number of questions not answered
     - `pos_ans`: Total positive answers
     - `positive_percent`: Percentage of positive answers
     - `dont_know_percent`: Percentage of unanswered questions

  7. Retrieve the first parent question for the evaluation. If not found, display an error message.

  8. Get all reports with the last answer related to the first parent question.

  9. Paginate the reports for display.

  10. Construct a URL for a button linked to the last report.

  11. Prepare the context for rendering the user profile page.

- If no reports are found for the user:
  - Display links to various sections that users can explore.

- Meta data is prepared for the page, including title, description, tags, and image.

- The context is updated with the prepared meta data.

- Finally, the view renders the user profile page with the provided context.

Documentation
--------------

- The function is documented using docstrings, explaining its purpose, inputs, and outputs.

- Comments within the code provide additional explanations about specific code sections and their functionality.

- Various sections of the code are explained in detail to provide better understanding.

- Comments and explanations are provided for context variables and calculations.

Usage Recommendations
----------------------

- This view function should be used within a Django application where user profiles and reports are managed.

- Developers should ensure that the required models and utilities are imported and configured properly before using this function.

- To maintain security, ensure that the `@login_required` decorator is applied to this view function to restrict access to authenticated users only.

- Developers can modify the context variables and calculations to customize the content and presentation of the user profile page as per their project requirements.

Note
----

- This documentation is provided as an explanatory guide and may need to be adapted based on the specific use case and context of the project.



Username Check Function
=======================

Check the availability and validity of a username in a signup form.

This function takes a POST request containing a 'username' parameter
and checks if the provided username is valid and available for registration.

Function Signature
------------------

.. code-block:: python

    def check_username(request):
        """
        Check the availability and validity of a username in a signup form.

        Args:
            request (HttpRequest): A POST request containing the 'username' parameter.

        Returns:
            HttpResponse: A response indicating whether the username is valid and available.
                - If the username contains spaces, returns a danger message.
                - If the username already exists in the User model, returns a danger message.
                - If the username is valid and available, returns a success message.
        """

Function Parameters
--------------------

- ``request`` (HttpRequest):
    A POST request containing the 'username' parameter.

Function Behavior
-----------------

1. Retrieve the username from the POST request.
2. Check for spaces in the username.
   - If spaces are found, return a danger message.
3. Check if the username already exists in the User model.
   - If the username already exists, return a danger message.
4. If the username is valid and available, return a success message.

Usage Example
-------------

.. code-block:: python

    from django.http import HttpRequest, HttpResponse
    from myapp.models import User  # Replace with actual import

    def check_username(request):
        # Your implementation here



check_email View Function
=========================


   Checks the validity and availability of an email address provided in a sign-up form.

   This function takes a POST request containing an email address from a sign-up form
   and performs the following checks:

   1. Validates the email format using Django's `django.core.validators.validate_email` function.
   2. Checks if the email address already exists in the User model.

   If the email is valid and not already taken, it returns a success message. If the
   email is invalid, already taken, or an exception occurs during validation, it returns
   an appropriate error message.

   :param HttpRequest request: The HTTP request containing the email in the POST data.
   :return: A response indicating the validity and availability of the email.
   :rtype: HttpResponse

   :raises: None

   Example::

       from django.core.validators import validate_email

       email = request.POST.get('email')
       try:
           validate_email(email)
           if User.objects.filter(email=email).exists():
               return HttpResponse('<span class="text-danger">This email already exists!</span>')
           else:
               return HttpResponse('<span class="text-success">This email available!</span>')
       except:
           return HttpResponse('<span class="text-danger">Type a valid email address!</span>')


partner_service View Function
=============================

.. code-block:: python

    @login_required
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def partner_service(request, pk):
        """
        Display the personalized service page for a partner user.
        
        This view displays the personalized service page for a visiting partner user. It retrieves the necessary information
        such as next activities and selected activities to be displayed on the page. It also handles visibility permissions
        based on the user's role (expert, staff, superuser). Additionally, it generates meta data for SEO purposes.
        
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the visiting user.
            
        Returns:
            HttpResponse: Rendered HTML template displaying the service page.
        """
        # To avoid circular reference
        from evaluation.models import NextActivities
        

Description
-----------

The `partner_service` view function is responsible for displaying a personalized service page for visiting partner users. It retrieves essential information such as next activities and selected activities to be shown on the page. This view also handles visibility permissions based on the user's role (expert, staff, superuser) and generates metadata for SEO purposes.

Parameters
----------

- `request` (HttpRequest): The HTTP request object.
- `pk` (int): The primary key of the visiting user.

Returns
-------

HttpResponse: Rendered HTML template displaying the service page.

Functionality
-------------

1. Retrieves the visiting user based on the provided primary key.
2. Retrieves the currently logged-in user.
3. Retrieves all next activities with prefetch for related 'quotnextactivity'.
4. Gets the selected activities of the visiting user.
5. Notifies the admin if there are no next activities and the current user is an expert.
6. Determines whether the visiting user's role allows visibility of certain blocks.
7. Creates a dictionary containing context data to be passed to the template.
8. Generates metadata for SEO and page information.
9. Updates the context with the generated metadata.
10. Renders the template with the provided context.

Usage
-----

1. Apply `@login_required` and caching decorators to the view function.
2. Call the `partner_service` function with the `request` and `pk` parameters to display the personalized service page for a partner user.

Note: Make sure to handle imports, mail sending, and any other dependencies properly for the view to work correctly in your project.



Commit Service View
===================

The `commit_service` view function is responsible for handling the process of users committing to a service, specifically related to next activities. This view enforces user authentication and certain permissions to ensure the ethical use of the application.

Functionality
-------------

The `commit_service` view follows a step-by-step process to achieve its goals:

1. User Authentication and Permissions
   - The user is required to be logged in. If not, an error message is returned indicating the unauthenticated operation as unethical.

2. Fetching Data
   - The function retrieves a list of active next activities, along with their associated details. This data is fetched using the `NextActivities` model.

3. Verification of User and Next Activity
   - The function verifies that the provided `user_id` corresponds to the currently logged-in user. If not, an error message is returned as the operation would be considered unethical.
   - It also verifies the existence and validity of the provided `na_id` by querying the `NextActivities` model. If the next activity doesn't exist, an error message is returned.

4. Recording User's Commitment
   - The function checks whether the user has already committed to the specified next activity. If not, a new record is created in the `UsersNextActivity` model to associate the user with the next activity.

5. Preparing Data for Rendering
   - Based on the user's permissions, the `block_visible` flag is determined. If the user is an expert, staff, or superuser, the flag is set to `True` to indicate that certain blocks should be visible.
   - Data including the visiting user, current user, list of next activities, next activities in which the user has already committed, and the `block_visible` flag are organized to be passed to the template.

6. Rendering the Template
   - The final step involves rendering the `commit_service.html` template with the prepared context data.

Permissions
-----------
The function enforces the following permissions:
- The user must be logged in.
- The user must have the `expert_required` decorator, indicating they have a certain level of expertise to perform the action.

Ethical Operation
-----------------
The view ensures ethical operation by checking user authentication, permissions, and the validity of the provided data. Any deviation from these criteria results in error messages that indicate an unethical operation.

Usage
-----
To use the `commit_service` view, provide the `user_id` and `na_id` as URL parameters. For instance, to commit a service for user with ID 123 and next activity ID 456:


Make sure to include the required URL patterns in your project's URL configuration to map to the `commit_service` view.

Requirements
-------------
- Django: This view relies on the Django framework for web application development.
- Models and Decorators: This view assumes the existence of models such as `NextActivities`, `UsersNextActivity`, and decorators like `login_required` and `expert_required`.

Please note that this documentation assumes familiarity with Django concepts and practices. If you encounter any issues or have questions, consult the Django documentation or seek assistance from experienced developers.



Delete Service View
===================

This view function enables expert users to delete a specific Next Activity associated with a visiting user.

Usage
-----

To use this view, ensure that the user is logged in and has expert privileges. The function is decorated with the ``@login_required`` and ``@expert_required`` decorators to ensure the required permissions are met.

Parameters
----------
- ``request`` (HttpRequest): The HTTP request object.
- ``user_id`` (str): The ID of the visiting user.
- ``na_id`` (str): The ID of the Next Activity to be deleted.

Returns
-------
``HttpResponse``: A rendered HTML response displaying the result of the operation.

Behavior
--------
1. If the ``user_id`` is 'None', a message is returned indicating unethical operation due to not being logged in.
2. Otherwise, the function retrieves the visiting user's details and validates their access permissions.
3. The function fetches the list of active Next Activities and their related quotnextactivity objects.
4. It checks if the current user has the permission to delete Next Activities. If not, a message about unethical operation is returned.
5. The target Next Activity to be deleted is fetched, and if not found, an unethical operation message is returned.
6. The target Next Activity is deleted.
7. The visibility of a certain block is determined based on the current user's role (expert, staff, or superuser).
8. Data is prepared to be sent to the template, including visiting user details, current user details, available next activities, next activities associated with the visiting user, and block visibility status.
9. The context is updated with the prepared data.
10. The template ``registration/commit_service.html`` is rendered using the context, and the HTML response is returned.

Please note that the decorators and exception handling are in place to ensure that only authorized users can perform this action, and the function takes care of various edge cases to prevent unethical operations.

Example Usage
-------------
Assuming a logged-in expert user with appropriate permissions, the URL might look like this::

    /delete-service/<user_id>/<na_id>/

where ``<user_id>`` and ``<na_id>`` should be replaced with the appropriate values.

Dependencies
------------
- This function depends on the Django framework and specific models and decorators within the application.

See Also
--------
- `Django Documentation <https://docs.djangoproject.com/en/stable/>`_
- `Django Login Required <https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator>`_
- `Custom Decorators in Django <https://djangocentral.com/creating-custom-decorators-in-django/>`_

``expert_required`` Decorator
-----------------------------
The ``@expert_required`` decorator is a custom decorator that checks whether the current user is an expert or has appropriate permissions before allowing access to the view. It can be defined as follows:

  .. code-block:: python

    def expert_required(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and (request.user.is_expert or request.user.is_staff or request.user.is_superuser):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You do not have permission to access this page.')
        return _wrapped_view


## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.

## License

This code is provided under the [MIT License](LICENSE).

## Credits


This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).
