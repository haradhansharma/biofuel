======================================================
README for 'custom_tags.py' in the 'templatetags' Directory of the 'Evaluation' App
======================================================

Introduction
------------

The 'custom_tags.py' module in the 'templatetags' directory of the 'Evaluation' app contains custom template filters and tags that extend the functionality of Django templates. These filters and tags are designed to enhance template rendering and provide additional features for template-based operations. This README provides an overview of the custom filters and tags available in this module.

Custom Filters and Tags Overview
---------------------------------

1. **brek_after_two Filter**:

    - This custom filter inserts a line break into text after a specified number of characters.
    - Usage Example:
      ```html
      {{ text|brek_after_two:10 }}
      ```

2. **get_verbose_name Tag**:

    - This custom template tag retrieves the verbose name of a field in a model.
    - Usage Example:
      ```html
      {% get_verbose_name instance field_name %}
      ```

3. **in_quot Filter**:

    - This filter filters quotes based on a specific user, returning only quotes associated with that user.
    - Usage Example:
      ```html
      {{ quotes|in_quot:user }}
      ```

4. **offchars Filter**:

    - This filter returns characters from the end of a string, excluding the specified number of characters from the beginning.
    - Usage Example:
      ```html
      {{ text|offchars:5 }}
      ```

5. **onnchars Filter**:

    - This filter returns characters from the beginning of a string, excluding the specified number of characters from the end.
    - Usage Example:
      ```html
      {{ text|onnchars:5 }}
      ```

6. **listobj_for_paginator Filter**:

    - This filter paginates a list of objects and returns a paginated Page object.
    - Usage Example:
      ```html
      {{ object_list|listobj_for_paginator:request }}
      ```

7. **get_options Filter**:

    - This filter retrieves options associated with a question and returns them as a list.
    - Usage Example:
      ```html
      {{ question|get_options }}
      ```

8. **get_quotations_user Filter**:

    - This filter retrieves quotations related to a question for a specific user and returns them as a list.
    - Usage Example:
      ```html
      {{ question|get_quotations_user:user }}
      ```

9. **get_related_quotations_user Filter**:

    - This filter retrieves related quotations for a question for a specific user and returns them as a list.
    - Usage Example:
      ```html
      {{ question|get_related_quotations_user:user }}
      ```

10. **get_merged_quotations_with_user Filter**:

    - This filter retrieves merged quotations for a question with a specific user and returns them as a list.
    - Usage Example:
      ```html
      {{ question|get_merged_quotations_with_user:user }}
      ```

Usage Instructions
------------------

To use the custom filters and tags defined in 'custom_tags.py' within your Django templates, follow these steps:

1. Import the necessary tags and filters in your template using `{% load custom_tags %}`.

2. Use the custom filters and tags as shown in the usage examples above within your template code.

Ensure that you include appropriate error handling and context variables in your templates when using these custom filters and tags.


=========================
Evaluation App - admin.py
=========================

This README provides an overview of the admin.py file for the Evaluation app. The admin.py file contains the Django admin configurations for various models within the app.

**Admin Configurations**

1. **QuestionAdmin**
   - Displays a list of questions with sorting and filtering options.
   - Includes inlines for Labels and Options related to questions.
   - Custom CSS styling is applied to the admin view.
   - Custom change list template to display error notes about question configurations.
   - Custom changelist_view method to add context data about questions with incomplete configurations.

2. **OptionAdmin**
   - Displays a list of options with filtering options.
   - Inherits from ExportActionMixin to provide export functionality.

3. **BiofuelAdmin**
   - Provides inlines for StdOils.

4. **EvaLebelStatementAdmin**
   - Displays a list of evaluation label statements with filtering options.

5. **StdOilsAdmin**
   - Displays a list of standard oils with inlines for StandaredCharts.
   - Custom CSS styling is applied to the admin view.

6. **SuggestionsAdmin**
   - Displays a list of suggestions with filtering and search options.
   - Provides readonly_fields for certain fields.

7. **LogicalStringAdmin**
   - Displays a list of logical strings with inlines for LsLabels.
   - Custom change list template to display error notes about logical string configurations.
   - Custom changelist_view method to add context data about logical strings with incomplete configurations.

8. **EvaluatorAdmin**
   - Displays a list of evaluators with filtering options.
   - Provides actions to generate updated reports and notify creators.
   - Custom check_and_notify method to execute the custom action.
   - Provides readonly_fields for certain fields.

9. **StandaredChartAdmin**
   - Displays a list of standard charts with filtering and editing options.
   - Custom CSS styling is applied to the admin view.

10. **NextActivitiesAdmin**
    - Provides an action to duplicate selected activities.
    - Provides readonly_fields for certain fields.

**Please Note**: The code comments and docstrings in admin.py provide further details about the functionality and purpose of each admin class.

If you have any questions or need additional information, please refer to the comments in the code or feel free to ask for assistance.


====================
Evaluation App - apps.py
====================

This README provides an overview of the apps.py file for the Evaluation app. The apps.py file contains the configuration settings for the 'evaluation' app.

**App Configuration**

- `default_auto_field`: Specifies the name of the default auto-generated primary key field.
- `name`: Specifies the name of the app.

**ready() Method**

The `ready()` method is executed when the app is ready to function within the Django project. In this method, the `evaluation.signals` module is imported, allowing the app to utilize signals for event handling.

**Example Usage**

To use this AppConfig in your Django project, add it to the 'INSTALLED_APPS' list in your project's settings.py file. This configuration ensures that the 'evaluation' app is integrated into your project and that its signals are loaded and available for use.

  ```python
  INSTALLED_APPS = [
      ...
      'evaluation',
      ...
  ]
  ```

========================
Evaluation App - middleware.py
========================

This README provides an overview of the middleware.py file for the Evaluation app. The middleware.py file contains the `EvaMiddleware` class, which is responsible for handling specific requests and sessions within the app.

**Middleware Overview**

Middleware in Django is used to process requests and responses globally before they reach the view or after they leave the view. This custom middleware class, `EvaMiddleware`, performs specific actions based on conditions before allowing a request to proceed to the view.

**Middleware Functionality**

- **Initialization**: The `__init__` method initializes the middleware with the provided `get_response` function.

- **Request Handling**: The `__call__` method is the main method of the middleware, called for each incoming request. It checks conditions and manages sessions before allowing the request to proceed to the view.

**Usage**

To use this middleware, add it to the `MIDDLEWARE` list in your Django project's `settings.py` file as follows:

  ```python
  MIDDLEWARE = [
      ...
      'evaluation.middleware.EvaMiddleware',
      ...
  ]
  ```

**Conditions Checked**

The middleware checks the following conditions before processing a request:

1. If the 'evaluator' key is present in the request session.
2. Whether a specific setting ('CNN') is enabled in the project's settings.

**Customization**

Do not customize the `EvaMiddleware` class. It can cause in the evaluation process and report genaration.



========================
Evaluation App - forms.py
========================

This README provides an overview of the forms.py file for the Evaluation app. The forms.py file contains the `EvaluatorForm` class, which is a Django form used for creating and updating Evaluator instances.

**Form Overview**

Forms in Django are used to handle user input and validation. The `EvaluatorForm` class is designed to work with the Evaluator model and provides a structured way to create and update Evaluator objects.

**Form Functionality**

- **Meta Class**: The inner `Meta` class defines metadata for the form, including the model and form fields. It also customizes labels for form fields.

- **Custom Validation**: The `clean` method is a custom form validation method that ensures the 'biofuel' selection is mandatory. If 'biofuel' is not selected, a validation error is raised.

**Form Fields**

The `EvaluatorForm` includes the following fields:
- 'name': Name of the evaluator.
- 'email': Email address of the evaluator.
- 'phone': Phone number of the evaluator.
- 'organization': Organization to which the evaluator belongs.
- 'biofuel': A dropdown field to select a fuel type.

**Form Widgets and Labels**

Form fields are customized with widgets to control their appearance in the HTML form. Custom labels are defined to provide clear field descriptions.

**Usage**

Developers can use this form in their views to create and update Evaluator instances. After binding the form to request data, validation can be performed, and Evaluator instances can be saved or updated based on user input.

**Customization**

Developers can customize this form to suit their app's specific needs by modifying form fields, widgets, labels, or adding additional validation logic.

If you have any questions or need further clarification, please refer to the comments in the code or feel free to ask for assistance.







Contributing
------------

Contributions to the 'Evaluation' app are welcome! If you'd like to contribute, please review the contribution guidelines in the project's repository.

License
-------

This module is distributed under the [Insert License Here] license. See the `LICENSE` file for more information.
