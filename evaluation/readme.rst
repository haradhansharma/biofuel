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



========================
Evaluation App - helper.py
========================

This README provides an overview of the helper.py file in the Evaluation app. The helper.py file contains various functions that retrieve and cache data from the database to improve performance on subsequent calls.

**Function Overview**

The helper functions in helper.py are designed to efficiently fetch and cache specific data from the database. Each function focuses on retrieving a specific set of data related to Questions, StdOils, or Glossary.

**Function Details**

- **`get_all_questions()`**: 
    - This function retrieves and caches all Question instances from the database.
    - It first checks the cache for the presence of cached questions to avoid unnecessary database queries.
    - If the cached data is not available, it fetches all Question instances, including related data, and caches the result for future use.
    - The cached data is stored for 3600 seconds (1 hour) to balance data freshness and query performance.

- **`get_all_stdoils()`**:
    - This function retrieves and caches all StdOils instances from the database.
    - Similar to `get_all_questions()`, it checks for cached data and fetches StdOils instances with related data if not already cached.
    - The cached data is also stored for 3600 seconds.

- **`get_all_glossaries()`**:
    - This function retrieves and caches all Glossary instances from the database.
    - Like the previous functions, it checks the cache for existing data and fetches Glossary instances if needed.
    - Cached data is stored for 3600 seconds.

- **`get_all_definedlabel()`**:
    - This function retrieves and caches all DifinedLabel instances from the database.
    - It follows a similar pattern as previous functions, checking for cached data and fetching DifinedLabel instances if not already cached.
    - Cached data is stored for 3600 seconds.

- **`get_all_reports_with_last_answer(request, first_of_parent)`**:
    - This function retrieves and caches reports (evaluators) with their last answered questions.
    - It accepts two arguments: `request` (the HTTP request object) and `first_of_parent` (the first question of the parent questionnaire).
    - The function distinguishes between superusers or staff and regular users when fetching reports.
    - For each report, it determines the last answered question and stores its slug.
    - Cached data is stored for 3600 seconds.

- **`get_biofuel()`**:
    - This function retrieves and caches all Biofuel instances from the database.
    - Similar to other functions, it checks for cached data and fetches Biofuel instances if needed.
    - Cached data is stored for 3600 seconds.

- **`get_options_of_ques(question)`**:
    - This function retrieves and caches all options related to a specific question.
    - It accepts a `question` argument (the question for which options are retrieved).
    - Cached data is stored using a key based on the question's ID and is stored for 3600 seconds.

- **`get_sugestions_of_ques(question)`**:
    - This function retrieves and caches all suggestions related to a specific question.
    - It accepts a `question` argument (the question for which suggestions are retrieved).
    - Suggestions are ordered by creation date.
    - Cached data is stored using a key based on the question's ID and is stored for 3600 seconds.

- **`active_sessions()`**:
    - This function retrieves evaluator IDs from active sessions in the past 24 hours.
    - It uses Django's `Session` model to fetch sessions that have not expired within the last 24 hours.
    - Active evaluator IDs are stored in a set to ensure uniqueness.
    - The function returns a list of evaluator IDs.

- **`clear_evaluator()`**:
    - This function clears incomplete evaluators and their related data from the database.
    - It is designed to run as a scheduled background task (e.g., via a CRON job) to maintain a clean database.
    - Incomplete evaluators are those that were initialized but have no associated data and have not generated a report.
    - The function fetches incomplete evaluators, checks if they are active in sessions, and deletes them along with their related data.
    - The deletion sequence is carefully managed to avoid foreign key constraints.
    - The function returns the total number of incomplete evaluators deleted during the process.

- **`get_current_evaluator(request, evaluator_id=None)`**:
    - This function retrieves the current evaluator object based on the provided `evaluator_id` or the `evaluator_id` stored in the user's session.
    - It is assumed that the middleware ensures 'evaluator' exists in the session.
    - Developers can use this function to retrieve the current evaluator or a specific evaluator by ID.
    - If no evaluator is found, it logs a debug message indicating the issue.


Below provides detailed information on the `EvaLebelStatementAnalyzer` class in the Evaluation app's helper.py file. The class is responsible for analyzing evaluation statements related to EvaLebel and generating assessment statements based on various criteria related to EvaLebel evaluations.

**Class Details**

- **`EvaLebelStatementAnalyzer`**:
    - A class for analyzing evaluation statements related to EvaLebel.
    - Provides methods for generating assessment statements based on various criteria.
    - Accepts two arguments during initialization: `evalebel` (an instance of EvaLebel representing the evaluation label) and `evaluator` (an instance representing the evaluator).

**Methods**

- **`get_statement_count(values_key, **filter_kwargs)`**:
    - Get the count of distinct statements based on filtering criteria.
    - Accepts a `values_key` for grouping and counting and additional filter criteria as keyword arguments.
    - Returns the count of distinct statements based on the filter criteria.

- **`get_dont_know_statement(label_name, value_count)`**:
    - Generate a statement based on the value count for "don't know" evaluations.
    - Accepts `label_name` (the name of the evaluation label) and `value_count` (the count of "don't know" evaluations).
    - Returns a statement describing the assessment based on the value count.

- **`get_positive_statement(label_name, value_count)`**:
    - Generate a statement based on the value count for positive evaluations.
    - Accepts `label_name` (the name of the evaluation label) and `value_count` (the count of positive evaluations).
    - Returns a statement describing the assessment based on the value count.

- **`ans_to_the_label()`**:
    - Get the count of answers related to the evaluation label.
    - Returns the count of answers related to the evaluation label.

- **`calculate_percentage(ans_to_the_lavel)`**:
    - Calculate the percentage based on answers related to the evaluation label.
    - Accepts `ans_to_the_label` (the count of answers related to the evaluation label).
    - Returns the percentage calculated based on the given count.

- **`label_assessment_for_donot_know()`**:
    - Generate an assessment statement for "don't know" evaluations related to the label.
    - Returns an assessment statement based on "don't know" evaluations.

- **`label_assessment_for_positive()`**:
    - Generate an assessment statement for positive evaluations related to the label.
    - Returns an assessment statement based on positive evaluations.

- **`ans_ques()`**:
    - Get the count of answerable questions.
    - Returns the count of answerable questions.

- **`calculate_overall_percent(ans)`**:
    - Calculate the overall percentage based on the given count.
    - Accepts `ans` (the count used to calculate the overall percentage).
    - Returns the overall percentage calculated based on the given count.

- **`overall_assessment_for_donot_know()`**:
    - Generate an overall assessment statement for "don't know" evaluations.
    - Returns an overall assessment statement based on "don't know" evaluations.

- **`overall_assessment_for_positive()`**:
    - Generate an overall assessment statement for positive evaluations.
    - Returns an overall assessment statement based on positive evaluations.

**Usage and Customization**

The `EvaLebelStatementAnalyzer` class is designed to analyze and generate assessment statements for EvaLebel evaluations. Developers can use its methods to provide valuable insights and feedback to evaluators.

Each method has specific functionality and can be customized as needed to tailor assessment statements based on different criteria and scenarios.

For more information about the usage of these methods and customizations, please refer to the code comments or reach out for further assistance.


Below README focusing on a class named `LabelWiseData`. This class is designed to handle various data calculations and retrievals related to label-wise evaluation.

**Class Details**

- **`LabelWiseData`**:
    - This class is designed to perform label-wise data calculations and retrievals.
    - The class is initialized with an `evaluator`, which can be obtained from the session or URL.

    **Properties**:

    - **`answered_question_id_list`**: Gets a list of unique answered question IDs.
    - **`total_active_questions`**: Gets the total count of active questions with four labels.
    - **`answered_percent`**: Calculates the percentage of answered questions out of total active questions.
    - **`total_positive_answer`**: Gets the total count of positive answers.
    - **`total_nagetive_answer`**: Gets the total count of negative answers.
    - **`overview_green`**: Calculates the percentage of positive answers out of total active questions.
    - **`overview_red`**: Calculates the percentage of negative answers out of total active questions.
    - **`overview_grey`**: Calculates the percentage of answers that are neither positive nor negative out of total active questions.

    **Methods**:

    - **`total_result()`**: Gets the overall results in a dictionary format, considering green, grey, and red as stackable bars.

    - **`label_wise_positive_answered(label)`**: Gets the count of positive answers for a specific label.

    - **`label_wise_nagetive_answered(label)`**: Gets the count of negative answers for a specific label.

    - **`label_wise_result()`**: Gets label-wise results in a dictionary format.

    - **`picked_labels_dict()`**: Gets a dictionary containing picked labels' results and the overall result.

    - **`packed_labels()`**: Creates a DataFrame from the picked labels' results. It's used to extract rows for use in JS's series.

    - **`label_data_history()`**: Gets historical label data as a list of dictionaries.

**Usage and Customization**

The `LabelWiseData` class is a powerful tool for calculating and retrieving label-wise evaluation data. Developers can use the properties and methods provided by this class to perform various data calculations, such as percentages, counts, and historical data.

While the class is designed for general use, developers can customize its behavior or extend its functionality to meet specific requirements. This flexibility allows for a wide range of data analysis and reporting possibilities.

For more details about how to use these properties and methods effectively, please refer to the code comments or reach out for further assistance.


Below README  focusing on the `nreport_context` function and its purpose in generating comprehensive PDF report contexts for evaluators.

**Function Details**

- **`nreport_context(request, slug)`**:
    - This function generates a comprehensive PDF report context for a given evaluator.
    - It accepts two arguments: `request` (the HTTP request object) and `slug` (the unique identifier of the evaluator).
    - The function performs various tasks to prepare the context for generating a report PDF:
        - Clears the `evaluator` session variable to allow editing the report.
        - Clears unnecessary session variables for completed reports.
        - Retrieves the evaluator report using the provided slug.
        - Creates a `LabelWiseData` instance for the evaluator.
        - Generates data for the PDF report, including label data and label data history.
        - Retrieves evaluation data for the evaluator.
        - Retrieves evaluator labels and statements.
        - Retrieves ordered next activities for the evaluator.
        - Calculates the percentage of answered questions for the report.
        - Determines the status of next activities (completed, not completed, not started, or unknown).
        - Prepares the report context dictionary, including evaluation data, labels, statements, next activities, and more.

**Usage and Customization**

The `nreport_context` function is a critical component for generating PDF reports for evaluators in the Evaluation app. Developers can use this function to create comprehensive report contexts tailored to their specific requirements.

The function is designed to retrieve data, perform calculations, and organize it into a context dictionary that can be passed to PDF generation functions or templates.

While the provided code is a substantial part of the PDF report generation process, developers can further customize and extend it to meet their specific reporting needs. The code includes comments to help developers understand each step of the process.

For more details about how this function works, please refer to the code comments or reach out for further assistance.


This README provides an overview of the last two functions in the helper.py file of the Evaluation app.

**Function Details**

- **`get_sugested_questions(request)`**:
    - This function retrieves suggested questions submitted by the current user.
    - It accepts a `request` argument, which contains user information.
    - The function filters Suggestions objects based on the current user, type 'question,' and no associated question.
    - The resulting QuerySet contains suggested questions submitted by the user.

- **`get_picked_na(question)`**:
    - This function retrieves active next activities that involve a specific question.
    - It accepts a `question` argument (the Question object to check for inclusion in next activities).
    - The function first retrieves all active NextActivities objects.
    - It then iterates through these next activities and checks if the specified question is involved.
    - The function returns a list of active NextActivities objects that include the specified question.

**Usage and Customization**

Developers can use these functions to retrieve and work with suggested questions and active next activities involving specific questions.

- `get_sugested_questions(request)`: Developers can call this function to retrieve suggested questions submitted by the current user. It is useful for managing user-generated content.

- `get_picked_na(question)`: This function helps developers find active next activities related to a particular question. It can be useful for determining the flow of activities based on user responses.

Customization of these functions may be required to meet specific project requirements. Developers can refer to code comments for more details on how these functions work.

For any further assistance or information on using these functions, please consult the code comments or contact the development team.




=======================
Evaluation App - signals.py
=======================

This README provides comprehensive information about the signals.py module in the Evaluation app, including the purpose of the signals, their usage, and customization options.

**Signals Overview**

The signals.py module contains custom signals and signal handlers used to perform specific actions during database transactions. Signals are a way to allow certain senders to notify a set of receivers that an action has taken place. In this context, the signals are used for database-related actions and provide flexibility in managing data changes.

**Signal: on_transaction_commit(func)**

- This custom signal is implemented as a decorator (`on_transaction_commit`) that wraps a function.
- Purpose: To execute a function after a database transaction is committed, ensuring that the function runs only when changes to the database are finalized.
- Args:
    - `func` (callable): The function to be executed after the transaction is committed.
- Usage: The decorator `@on_transaction_commit` can be applied to functions that need to run after database transactions.
- Customization: Developers can use this decorator to create functions that respond to specific database changes once they are confirmed.

**Signal: delete_option_sets(sender, instance, **kwargs)**

- This signal handler is executed when a `LogicalString` instance is deleted.
- Purpose: To delete associated `OptionSet` objects when a `LogicalString` is deleted, ensuring proper data cleanup.
- Args:
    - `sender`: The sender of the signal (`LogicalString`).
    - `instance`: The instance of the `LogicalString` being deleted.
    - `**kwargs`: Additional keyword arguments.
- Usage: This signal handler is automatically triggered when a `LogicalString` is deleted, and it takes care of deleting related `OptionSet` instances.
- Customization: Developers can customize this signal handler to perform additional actions or validations during `LogicalString` deletion.

**Signal: recreate_option_sets(sender, instance, **kwargs)**

- This signal handler is executed when a `LogicalString` instance is saved or updated.
- Purpose: To recreate `OptionSet` objects based on changes in `LogicalString`, ensuring that the two are synchronized.
- Args:
    - `sender`: The sender of the signal (`LogicalString`).
    - `instance`: The instance of the `LogicalString` being saved.
    - `**kwargs`: Additional keyword arguments.
- Usage: This signal handler is automatically triggered when a `LogicalString` is saved or updated. It collects saved logical strings, compares them with existing `OptionSet` instances, and ensures synchronization.
- Customization: Developers can modify this signal handler to include additional logic or conditions based on project requirements.


**Signal: add_question_to_the_oil(sender, instance, created, **kwargs)**

- This signal handler is executed when a new `OliList` instance is created.
- Purpose: To assign all active questions to the newly created oil, ensuring that questions are associated with the oil from the beginning.
- Args:
    - `sender`: The sender of the signal (`OliList`).
    - `instance`: The instance of the `OliList` being saved.
    - `created` (bool): True if a new object is created, False if an existing one is saved.
    - `**kwargs`: Additional keyword arguments.
- Usage: This signal handler is triggered when a new oil is created. It fetches all active questions and associates them with the oil using `StandaredChart` instances.
- Customization: Developers can customize this signal handler to include additional logic or conditions when associating questions with oils.

**Signal: on_option_change(sender, instance, **kwargs)**

- This signal handler is executed before saving an `Option` instance.
- Purpose: To detect changes in `Option` objects and notify evaluators accordingly.
- Args:
    - `sender`: The sender of the signal (`Option`).
    - `instance`: The instance of the `Option` being saved.
    - `**kwargs`: Additional keyword arguments.
- Usage: This signal handler is triggered when an `Option` is about to be saved. It checks for changes in the `Option` fields and updates the `feedback_updated` status for relevant evaluators.
- Customization: Developers can modify this signal handler to include additional checks, notifications, or conditions based on project requirements.

**Signal: add_to_the_user_next(sender, instance, created, **kwargs)**

- This signal handler is executed when a new `NextActivities` instance is created.
- Purpose: To add a `NextActivity` to a user's list of upcoming activities and send email notifications.
- Args:
    - `sender`: The sender of the signal (`NextActivities`).
    - `instance`: The instance of the `NextActivities` being saved.
    - `created` (bool): True if a new object is created, False if an existing one is saved.
    - `**kwargs`: Additional keyword arguments.
- Usage: This signal handler is triggered when a new `NextActivities` instance is created. It adds the activity to the user's list of upcoming activities and sends email notifications to the creator and other users involved.
- Customization: Developers can customize this signal handler to include additional notification methods, content, or recipients as needed.

**Signal Usage and Customization**

Developers can use these signals and signal handlers to automate actions, maintain data consistency, and respond to database changes effectively. By understanding the purpose and behavior of each signal, developers can customize them to meet specific project needs.

For further details on the usage, customization, and integration of these signals in your project, consult the code comments or reach out to the development team for assistance.



=======================
Evaluation App - models.py
=======================

This README provides comprehensive information about the `models.py` module in the Evaluation app, including the purpose of the defined models and any custom validators used.

**Custom Validator: get_common_status(value)**

- This custom validator is used to ensure that there is only one common status entry in `DefinedLabel` objects.
- Purpose: To validate that only one `DefinedLabel` object can have the `common_status` field set to `True`.
- Args:
    - `value`: The value to check (usually 1 for common status).
- Raises:
    - `ValidationError`: Raised if there is already a common status defined.
- Usage: This validator is applied to the `common_status` field of `DefinedLabel` models to prevent the creation of multiple common status entries.
- Customization: Developers can use this validator to enforce specific constraints on the `common_status` field as needed.

**Model: DefinedLabel**

- This model serves as a database connector for labels used site-wide.
- Labels are used in reports and question settings in the admin.
- Only one common status can exist.
- Fields:
    - `name`: A character field for the label's name (max length: 252).
    - `label`: A character field for additional label information (max length: 252, default: '').
    - `adj`: A character field for label adjustments (max length: 252, default: '').
    - `common_status`: A boolean field indicating whether this label is a common status, with a custom validator to ensure uniqueness.
    - `sort_order`: A character field for sorting the labels (max length: 3, default: 0).
- Usage: This model is used to define labels that are used throughout the application. It enforces the uniqueness of common status labels.
- Customization: Developers can extend this model or modify its fields to suit specific project requirements.

**Function: generate_uuid()**

- This function generates a hexadecimal code for slug URLs, currently used only on questions.
- Purpose: To generate a unique identifier for slug URLs.
- Usage: This function can be used wherever unique slugs are required, such as in question URLs.
- Customization: Developers can customize this function or its usage based on project needs.

For further details on the usage, customization, and integration of these models and validators in your project, consult the code comments or reach out to the development team for assistance.

**Model: Question**

- This model serves as a database connection for questions within the Evaluation app.
- Key Features:
    - `slug`: A unique character field (max length: 40) generated using `generate_uuid()` for slug URLs. Not editable.
    - `name`: A character field for the question's name (max length: 252).
    - `chapter_name`: A character field for the chapter name associated with the question (max length: 252, nullable).
    - `parent_question`: A foreign key reference to another `Question` instance, representing the parent question (self-referential, nullable).
    - `sort_order`: An integer field used for sorting questions (default: 1).
    - `description`: A text field for the question's description.
    - `is_active`: A boolean field indicating the question's active status (default: False).
    - `is_door`: A boolean field indicating whether the question is a "door" question (default: False).
    - `chart_title`: A character field for the chart title associated with the question (max length: 252, nullable).
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).
    - `update_date`: A datetime field indicating the last update date (auto-generated, nullable).

**Model Functions and Properties:**

- `get_absolute_url()`: Get the URL for browsing an individual question for editing (not used in the evaluation procedure).

- `add_quatation`: Get the URL for adding a quotation to the question.

- `labels`: Get labels related to this question.

- `get_related_quotations`: Get related quotations for this question.

- `get_quotations`: Get quotations associated with this question.

- `get_merged_quotations`: Get merged quotations, including related and associated quotations.

- `get_options`: Get options for this question.

- `get_stdoils`: Get standard oils associated with this question.

- `have_4labels()`: Check if the question has at least 4 labels.

- `problem_in_option`: Check for problems in question options.

- `not_is_door_nor_have_parent`: Check if the question is neither a door nor has a parent.

- `get_sugestions()`: Get suggestions related to this question.

**Additional Notes:**

- The `Question` model is used to represent questions and their properties within the Evaluation app.
- It provides various methods and properties to access related data and perform checks on question attributes.

For further details on the usage, customization, and integration of this model and its associated functions in your project, consult the code comments or reach out to the development team for assistance.


**Model: Label**

- This model serves as a database connection for labels.
- Key Features:
    - `name`: A foreign key reference to a `DifinedLabel` instance using `on_delete=models.PROTECT`, limiting choices to those with `common_status` set to `False`.
    - `question`: A foreign key reference to a `Question` instance using `on_delete=models.CASCADE`.
    - `value`: A character field (max length: 1) that follows business logic.
    
**Model: Option**

- This model serves as a database connection for options.
- Key Features:
    - `name`: A character field (max length: 252) for the option's name.
    - `yes_status`: A boolean field indicating whether the option represents 'Yes' (default: False).
    - `dont_know`: A boolean field indicating whether the option represents 'Don't Know' (default: False).
    - `question`: A foreign key reference to a `Question` instance using `on_delete=models.CASCADE`.
    - `next_question`: A foreign key reference to a `Question` instance (nullable) representing the next question during the evaluation process.
    - `statement`: A text field (nullable) for a statement printed under the label in the report and question page.
    - `next_step`: A text field (nullable) for the next step printed under the label based on business logic in report and question forms.
    - `overall`: A character field (max length: 1, default: 0) used to determine if the statement should be added to the summary.
    - `positive`: A character field (max length: 1, default: 0) used to calculate assessment under the label in the report and question form.
    
**Model: LogicalString**

- This model serves as a database connection for logical statements based on selected options.
- Key Features:
    - `options`: A many-to-many relationship with `Option` instances.
    - `text`: A text field (nullable) that acts as the statement.
    - `overall`: A character field (max length: 1, default: 0) used to determine if the statement should be added to the summary.
    - `positive`: A character field (max length: 1, default: 0) used to calculate assessment under the label in reports and question forms.

**Additional Notes:**

- The `Label`, `Option`, and `LogicalString` models are used to manage labels, options, and logical statements within the Evaluation app.
- These models have various fields and properties that are used to configure how labels, options, and statements are used in the evaluation process.

For further details on the usage, customization, and integration of these models in your project, consult the code comments or reach out to the development team for assistance.


**Model: OptionSet**

- This model is automatically generated during evaluation by the user and is not displayed in the admin side.
- Key Features:
    - `option_list`: A character field (max length: 252) that is unique and indexed, representing a list of options.
    - `text`: A text field for additional information.
    - `positive`: A character field (max length: 1, default: 0) used for positive assessments.
    - `overall`: A character field (max length: 1, default: 0) used for overall assessments.
    - `ls_id`: A character field (max length: 252, default: 0) for logical string identification.
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).
    - `update_date`: A datetime field indicating the last update date (auto-generated, nullable).

**Model: Lslabel**

- This model represents labels for logical strings to be selected during the setup of logical strings.
- Key Features:
    - `name`: A foreign key reference to a `DifinedLabel` instance using `on_delete=models.PROTECT`, limiting choices to those with `common_status` set to `False`.
    - `logical_string`: A foreign key reference to a `LogicalString` instance using `on_delete=models.CASCADE`.
    - `value`: A character field (max length: 1, default: 0) following business logic.

**Model: Biofuel**

- This model represents the biofuel selected by the user on the initial page of evaluation.
- Key Features:
    - `name`: A character field (max length: 252) representing the biofuel name.

**Model: Evaluator**

- This model is automatically generated during evaluation by the user and should not be edited or modified from the admin side.
- Key Features:
    - `slug`: A UUID field (auto-generated, unique, not editable, indexed) used for identification.
    - `creator`: A foreign key reference to a user using `on_delete=models.SET_NULL` (nullable).
    - `name`: A character field (max length: 252) representing the evaluator's name.
    - `email`: An email field for the evaluator's email address.
    - `phone`: A character field (max length: 16, nullable) for the evaluator's phone number.
    - `organization`: A character field (max length: 252, nullable) for the evaluator's organization.
    - `biofuel`: A foreign key reference to a `Biofuel` instance using `on_delete=models.SET_NULL` (nullable).
    - `stdoil_key`: A character field (max length: 20, nullable, indexed) representing a standard oil key.
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).
    - `update_date`: A datetime field indicating the last update date (auto-generated, nullable).
    - `report_generated`: A boolean field (default: False) indicating whether a report has been generated.
    - `feedback_updated`: A boolean field (default: False) indicating whether feedback has been updated.

**Model: Evaluation**

- This model is automatically generated during evaluation by the user and is not displayed in the admin side.
- Key Features:
    - `evaluator`: A foreign key reference to an `Evaluator` instance using `on_delete=models.RESTRICT`.
    - `option`: A foreign key reference to an `Option` instance using `on_delete=models.RESTRICT`.
    - `question`: A foreign key reference to a `Question` instance using `on_delete=models.RESTRICT` (nullable).

**Model: EvaComments**

- This model is automatically generated during evaluation by the user and is not displayed in the admin side.
- Key Features:
    - `evaluator`: A foreign key reference to an `Evaluator` instance using `on_delete=models.RESTRICT`.
    - `question`: A foreign key reference to a `Question` instance using `on_delete=models.RESTRICT`.
    - `comments`: A text field (max length: 600) for comments.

**Additional Notes:**

- These models are used for various aspects of the evaluation process within the Evaluation app.
- They are automatically generated during the evaluation and should not be modified directly through the admin interface.

For further details on the usage, customization, and integration of these models in your project, consult the code comments or reach out to the development team for assistance.

**Model: EvaLabel**

- This model is automatically generated during evaluation by the user and is not displayed in the admin side.
- Key Features:
    - `label`: A foreign key reference to a `DifinedLabel` instance using `on_delete=models.PROTECT`.
    - `evaluator`: A foreign key reference to an `Evaluator` instance using `on_delete=models.RESTRICT`.
    - `sort_order`: A character field (max length: 3, default: 0).
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).

**Model: EvaLabelStatement**

- This model is automatically generated during evaluation by the user and is not displayed in the admin side.
- Key Features:
    - `evalebel`: A foreign key reference to an `EvaLabel` instance using `on_delete=models.PROTECT`.
    - `question`: A foreign key reference to a `Question` instance using `on_delete=models.PROTECT` (nullable).
    - `option_id`: A character field (max length: 252, nullable).
    - `statement`: A text field for statements (nullable).
    - `next_step`: A text field for the next step (nullable).
    - `positive`: A character field (max length: 1, default: 0) for positive assessments.
    - `dont_know`: A boolean field (default: False) indicating 'Don't Know'.
    - `assessment`: A boolean field (default: False).
    - `next_activity`: A boolean field (default: False).
    - `evaluator`: A foreign key reference to an `Evaluator` instance using `on_delete=models.RESTRICT` (nullable).
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).
    - `update_date`: A datetime field indicating the last update date (auto-generated, nullable).

**Model: NextActivities**

- This model represents the main parameters for next activities.
- Key Features:
    - `name_and_standard`: A character field (max length: 250) representing the name and standard.
    - `short_description`: A text field (max length: 152) for a brief description.
    - `descriptions`: A text field for detailed descriptions.
    - `url`: A URL field (nullable).
    - `priority`: A character field (max length: 2) for specifying the sort order.
    - `related_questions`: A many-to-many relationship with `Question` instances for related questions (limit choices to those with `is_active` set to `True`).
    - `compulsory_questions`: A many-to-many relationship with `Question` instances for compulsory questions (limit choices to those with `is_active` set to `True`).
    - `related_percent`: An integer field (default: 90).
    - `compulsory_percent`: An integer field (default: 100).
    - `is_active`: A boolean field (default: True) for publishing.
    - `same_tried_by`: A JSON field (nullable).
    - `created_by`: A foreign key reference to the user who created this instance using `on_delete=models.CASCADE`.
    - `create_date`: A datetime field indicating the creation date (auto-generated, nullable).
    - `update_date`: A datetime field indicating the last update date (auto-generated, nullable).

**Additional Notes:**

- These models are used for various aspects of the evaluation process within the Evaluation app.
- They are automatically generated during the evaluation and should not be modified directly through the admin interface.

For further details on the usage, customization, and integration of these models in your project, consult the code comments or reach out to the development team for assistance.


**Model: EvaluatorActivities**

- This model represents Evaluator Activities.
- Attributes:
    - `evaluator` (ForeignKey): A reference to the associated evaluator using `on_delete=models.CASCADE`.
    - `next_activity` (ForeignKey): A reference to the next activity related to the evaluator using `on_delete=models.CASCADE`.
    - `related_percent` (IntegerField): Related percentage.
    - `compulsory_percent` (IntegerField): Compulsory percentage.
    - `is_active` (BooleanField): Indicates whether the activity is active or not.
    - `create_date` (DateTimeField): Date and time of creation (auto-generated, nullable).
    - `update_date` (DateTimeField): Date and time of the last update (auto-generated, nullable).
- Methods:
    - `__str__()`: Returns a string representation of the next activity's name and standard.

**Model: OliList**

- This model represents Defined Oils.
- Attributes:
    - `name` (CharField): The name of the defined oil (unique).
    - `key` (CharField): A unique key generated based on the name.
- Methods:
    - `__str__()`: Returns the name of the defined oil.
    - `save()`: Overrides the default save method to generate and save the key based on the name.

**Model: StdOils**

- This model represents Standard Oils.
- Attributes:
    - `select_oil` (ForeignKey): A reference to the selected oil from `OliList` using `on_delete=models.CASCADE`.
    - `biofuel` (ForeignKey): A reference to the associated biofuel (nullable).
- Methods:
    - `__str__()`: Returns the name of the selected oil.

**Model: StandaredChart**

- This model represents Standard Charts.
- Attributes:
    - `oil` (ForeignKey): A reference to the associated standard oil using `on_delete=models.CASCADE`.
    - `question` (ForeignKey): A reference to the associated question using `on_delete=models.CASCADE` (limit choices to those with `is_active` set to `True`).
    - `unit` (ForeignKey): A reference to the associated weight unit (nullable).
    - `value` (CharField): The value for the chart (nullable).
    - `link` (URLField): A URL link (nullable).
    - `option` (ChainedForeignKey): A reference to the associated option (nullable).
- Methods:
    - `oil_key()`: Returns the lowercase key of the associated standard oil.
    - `__str__()`: Returns the name of the associated standard oil.

**Additional Notes:**

- These models are used to represent various aspects of the evaluation process and standard chart information within the Evaluation app.
- Ensure that you follow the specific constraints and relationships defined in these models to maintain data integrity and functionality.
- Refer to the model methods for additional functionality and customization options.


**Model: Youtube_data**

- This model is used to store YouTube data for specific search terms.
- Attributes:
    - `term` (TextField): The search term for YouTube data.
    - `urls` (TextField): URLs related to the search term.
    - `create_date` (DateTimeField): Date and time of creation (auto-generated, nullable).
    - `update_date` (DateTimeField): Date and time of the last update (auto-generated, nullable).
- Methods:
    - `__str__()`: Returns the search term as a string.

**Model: LabelDataHistory**

- This model is used to store Label Data History.
- Attributes:
    - `evaluator` (ForeignKey): A reference to the associated evaluator using `on_delete=models.CASCADE`.
    - `items` (TextField): History of labeled items (limited to 250 characters).
    - `created` (DateTimeField): Date and time of creation (auto-generated, nullable).
- Methods:
    - `__str__()`: Returns the items history as a string.
- Meta:
    - `verbose_name`: 'Label Data History'
    - `verbose_name_plural`: 'Label Data Histories'

**Model: ReportMailQueue**

- This model is used to queue report mail sending tasks.
- Attributes:
    - `to` (CharField): Email address of the recipient.
    - `from_report` (ForeignKey): The sender (Evaluator) of the report using `on_delete=models.CASCADE`.
    - `new_report` (ForeignKey): The report being sent using `on_delete=models.CASCADE`.
    - `added_at` (DateTimeField): Date and time when the report was added to the queue (auto-generated).
    - `processed` (BooleanField): Indicates whether the task has been processed.
    - `process_time` (DateTimeField): Date and time of processing (auto-generated).
    - `tried` (IntegerField): Number of attempts to send the report.
- Methods:
    - `__str__()`: Returns the recipient's email address as a string.
- Note: The mail queues will be executed by crontab and are created during the saving of BlogPost.

**Model: Suggestions**

- This model is used to store user suggestions.
- Attributes:
    - `question` (ForeignKey): A reference to the associated question (nullable).
    - `su_type` (CharField): Type of suggestion ('question' or 'option').
    - `title` (CharField): Title of the suggestion.
    - `statement` (TextField): The suggestion statement.
    - `suggested_by` (ForeignKey to User): The user who suggested the idea.
    - `parent` (ForeignKey to self): The parent suggestion (nullable, used for replies).
    - `related_qs` (ForeignKey to self): Related suggestion (nullable, for cross-reference).
    - `comitted` (BooleanField): Indicates whether the suggestion has been committed.
    - `created` (DateTimeField): Date and time of creation (auto-generated).
    - `updated` (DateTimeField): Date and time of the last update (auto-generated).
- Methods:
    - `__str__()`: Returns the title of the suggestion.
- Meta:
    - `verbose_name`: 'Suggestion'
- Note: The 'question' field is nullable, allowing suggestions without an associated question.



=========================================================
ReportPDFData Class of nreport_class.py of EVALUATION APP
=========================================================

The `ReportPDFData` class is an essential part of the Evaluation APP, responsible for generating PDF reports based on evaluation data. This class initializes various styles and settings for formatting the PDF report, draws images and content on the pages, and organizes different sections of the report.

Initialization
---------------

To create a `ReportPDFData` object, you need to provide two parameters: `request` and `slug`. These parameters are required for constructing the report.

- `request`: The Django request object.
- `slug`: The slug for the Evaluator object.

Attributes
----------

This class has several attributes used for styling and formatting the report:

- `pagesize`: The page size (A4 by default).
- `PH` and `PW`: Page height and width.
- `M`: Margin size.
- `styles`: Sample styles for text formatting.
- `title`, `t_additional`, `author`, `creator`, and `producer`: Information about the report.
- `stylesN`, `stylesH1`, `stylesH2`, `stylesH3`, `stylesH4`, `stylesH5`, `stylesH6`, `stylesT`, `stylesB`: Styles for different text elements.
- `stylesB.alignment`: Text alignment.
- Custom paragraph styles like `TitleR`, `SectionT`, `LeftIndent`, and `Footer`.
- `stylesTR`, `SectionT`, `LeftIndent`, `Footer`: References to the custom paragraph styles.
- `title_font_size`: Font size for report titles.

Methods
-------

This class contains various methods to generate different parts of the PDF report, including:

- `report_initial(c, doc)`: Draws an initial image on the report's first page.
- `top_string(c, doc)`: Adds a top string with the project title to the report.
- Methods to create horizontal lines with different widths: `uline`, `uline34`, `uline100`, `ulineDG100`, and `ulineG100`.
- `first_page(c, doc)`: Generates the content for the first page of the report.
- `later_page(c, doc)`: Generates the content for pages after the first page of the report.
- `wrapped_pdf()`: Generates the content of the wrapped PDF report.
- `basic_summary()`: Generates the basic summary section of the report.
- `desclimar_and_content()`: Generates the disclaimer and content section of the report.
- `grape_status()`: Generates the grape status section of the report.
- `points_status()`: Generates the points status section of the report.
- `todos()`: Generates the list of todos section of the report.
- `summary_statement()`: Generates the summary statement section of the report.
- `question_specific_feedback()`: Generates the question-specific feedback section of the report.
- `details_of_activities()`: Generates the details of activities section of the report.
- `biofuel_history()`: Generates the biofuel history section of the report.

Usage
-----

To use the `ReportPDFData` class, you need to initialize an instance with the required parameters and then call the appropriate methods to generate the report content. The resulting content can be added to a PDF document.

Example Usage
-------------

  ```python
  # Initialize the ReportPDFData object
  report_data = ReportPDFData(request, slug)

  # Create a PDF document
  pdf_doc = SimpleDocTemplate("evaluation_report.pdf")

  # Generate the report content
  report_content = report_data.wrapped_pdf()

  # Build the PDF document with the report content
  pdf_doc.build(report_content)

  ```


=====================================
sitemaps.py - Evaluation APP Sitemaps
=====================================

This module defines sitemaps for the Evaluation APP within the GFVP (Green Fuel Validation Platform) website. Sitemaps are used to inform search engines about the structure and hierarchy of your site's URLs, helping improve SEO and discoverability.

GfvpSitemap
-----------

:class:`GfvpSitemap` is the main sitemap for the GFVP website. It includes various important URLs for the website.

Attributes:
    - `priority` (float): The priority of this sitemap in relation to others (0.0 to 1.0).
    - `changefreq` (str): The expected change frequency of URLs in this sitemap.

Methods:
    - `items()`: Define the list of URLs to include in the sitemap.
    - `location(item)`: Generate the URL for a given item using its name.

UserSitemap
-----------

:class:`UserSitemap` is responsible for sitemapping user profiles on the GFVP website. It includes user profiles who are active and have verified email addresses.

Attributes:
    - `changefreq` (str): The expected change frequency of URLs in this sitemap.
    - `priority` (float): The priority of this sitemap in relation to others (0.0 to 1.0).

Methods:
    - `items()`: Retrieve the list of active users with verified email addresses.
    - `lastmod(obj)`: Determine the last modification date for a user profile.
    - `location(obj)`: Generate the URL for a user's profile.

UserTypeSitemap
---------------

:class:`UserTypeSitemap` is responsible for sitemapping user types on the GFVP website. It includes active user types.

Attributes:
    - `changefreq` (str): The expected change frequency of URLs in this sitemap.
    - `priority` (float): The priority of this sitemap in relation to others (0.0 to 1.0).

Methods:
    - `items()`: Retrieve the list of active user types.
    - `lastmod(obj)`: Determine the last modification date for a user type.
    - `location(obj)`: Generate the URL for a user type page.

BlogSitemap
-----------

:class:`BlogSitemap` is responsible for sitemapping blog posts on the GFVP website. It includes published blog posts.

Attributes:
    - `changefreq` (str): The expected change frequency of URLs in this sitemap.
    - `priority` (float): The priority of this sitemap in relation to others (0.0 to 1.0).

Methods:
    - `items()`: Retrieve the list of published blog posts.
    - `lastmod(obj)`: Determine the last modification date for a blog post.
    - `location(obj)`: Generate the URL for a blog post.

HtmlReportSitemap
-----------------

:class:`HtmlReportSitemap` is responsible for sitemapping generated evaluation reports on the GFVP website. It includes evaluation reports with verified email addresses.

Attributes:
    - `changefreq` (str): The expected change frequency of URLs in this sitemap.
    - `priority` (float): The priority of this sitemap in relation to others (0.0 to 1.0).

Methods:
    - `items()`: Retrieve the list of generated evaluation reports.
    - `lastmod(obj)`: Determine the last modification date for an evaluation report.
    - `location(obj)`: Generate the URL for an evaluation report.

For detailed information on each sitemap class, their methods, and attributes, please refer to the code comments and docstrings provided within `sitemaps.py`.


=============================
urls.py - Evaluation APP URLs
=============================

This module defines the URL patterns for the Evaluation APP within the GFVP (Green Fuel Validation Platform) website. It also includes the configuration of sitemaps for various sections of the website.

Sitemaps Configuration
----------------------

The following sitemaps are configured for different sections of the website:

- `static`: Sitemap for static URLs
- `active_users`: Sitemap for active user profiles
- `user_types`: Sitemap for user types
- `blog_list`: Sitemap for blog posts
- `HtmlReportitemap`: Sitemap for HTML reports

URL Patterns
------------

The URL patterns are organized into two main sections: core patterns and additional patterns for the 'evaluation' app.

Core URL Patterns:
------------------

1. `evaluation/thanks/`: URL for the 'thanks' view.
2. `evaluation/report/<str:slug>`: URL for the 'report' view with a dynamic slug parameter.
3. `evaluation/nreport/<str:slug>`: URL for the 'nreport' view with a dynamic slug parameter.
4. `evaluation/nreport_pdf/<str:slug>`: URL for the 'nreport_pdf' view with a dynamic slug parameter.
5. `get-glossary/`: URL for the 'get_glossary' view.
6. `sitemap.xml/`: URL for the sitemap view, which uses Django's sitemap framework to generate sitemaps for search engines.

Additional URL Patterns for the 'evaluation' App:
-------------------------------------------------

1. `evaluation2/`: URL for the 'eva_index2' view.
2. `evaluation2/option_add/`: URL for the 'option_add2' view.
3. `evaluation2/<int:evaluator_id>/<str:slug>`: URL for the 'eva_question' view with dynamic parameters.
4. `evaluation/stdoils/`: URL for the 'stdoils' view.
5. `vedio_urls/<str:search_term>`: URL for the 'vedio_urls' view with a dynamic search_term parameter.
6. `std_oils_block/<str:slug>`: URL for the 'std_oils_block' view with a dynamic slug parameter.
7. `quotation_block/<str:slug>`: URL for the 'quotation_block' view with a dynamic slug parameter.
8. `traficlighthori/<str:last_reports>`: URL for the 'trafic_light_hori' view with a dynamic last_reports parameter.
9. `fuel-history/<str:last_reports>`: URL for the 'fuel_history' view with a dynamic last_reports parameter.

For more details on each URL pattern and its corresponding view, please refer to the code and comments provided within `urls.py`.



Contributing
------------

Contributions to the 'Evaluation' app are welcome! If you'd like to contribute, please review the contribution guidelines in the project's repository.

License
-------

This module is distributed under the [Insert License Here] license. See the `LICENSE` file for more information.
