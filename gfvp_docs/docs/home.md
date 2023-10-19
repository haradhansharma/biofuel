---
title: Technical Guide Home app of GFVP
summary: Here given overview of the home app of Green fuel validation platform.
copyright: (c) gf-vp.com
repo_url: https://github.com/haradhansharma/biofuel
edit_uri: blob/v24123/gfvp_docs/docs
authors:
    - Haradhan Sharma
date: 2023-10-16

---
# Home App - Django Project Skeleton


### Description

The "home" app is an integral part of the Django project. It includes various components that are essential for the functionality of the project. This readme provides an overview of the key components within the "home" app.

### Components

- `admin.py`: This module contains configurations for Django's admin interface, allowing administrators to manage data associated with the "home" app.

- `forms.py`: The forms module includes form classes used for user input validation and data submission within the app.

- `models.py`: In this module, the database models are defined, which represent the data structures and relationships for the "home" app.

- `views.py`: The views module contains view functions that handle user requests, process data, and render templates.

- `helper.py`: This module may include any utility functions or helpers used across the "home" app to streamline common tasks or logic.


## admin.py

- `admin.py`: This module contains configurations for Django's admin interface, allowing administrators to manage data associated with the "home" app. In this file, various models are registered with the Django admin site to provide an interface for administrators to manage data. The following models are registered:

    - `PriceUnit`: Registered with the Django admin site to manage price units.
    
    - `WeightUnit`: Registered with the Django admin site to manage weight units.
    
    - `TimeUnit`: Registered with the Django admin site to manage time units.
    
    - `QuotationDocType`: Registered with the Django admin site to manage quotation document types.
    
    - `Quotation`: Registered with the Django admin site to manage quotations.

  These registrations enable administrators to create, edit, and delete records related to these models using the Django admin interface.


## forms.py

This `forms.py` file defines custom form classes for various aspects of a web application. These form classes are designed to provide a more tailored and user-friendly experience for creating and editing user profiles, updating company logos, and managing questions.

1. `PasswordChangeForm`
   The `PasswordChangeForm` is a custom form for changing a user's password. It enhances the default Django `PasswordChangeForm` by updating the widget attributes to improve user experience. Specifically, it sets the autocomplete values for old and new passwords and assigns CSS classes for styling.

2. `UserForm`
   The `UserForm` is used for creating and editing user profiles. It is based on the Django `ModelForm` and is associated with the `User` model. The form fields are customized with placeholders, CSS classes, and ARIA labels to make the user interface more user-friendly.

3. `CompanyLogoForm`
   The `CompanyLogoForm` is designed for updating company logos in user profiles. It is also based on the `ModelForm` and is associated with the `Profile` model. It customizes the widget for the `company_logo` field, providing a user-friendly way to update the company's logo.

4. `ProfileForm`
   The `ProfileForm` is used for creating and editing user profiles. It is similar to the `UserForm` but focuses on fields related to a user's personal profile, such as about information, location, and establishment date. The form fields are customized with placeholders, CSS classes, and ARIA labels for improved user experience.

5. `QuestionForm`
   The `QuestionForm` is employed for creating and editing questions. It is associated with the `Question` model and customizes the widget for the `name` field. It also provides a more user-friendly experience by adding placeholders, CSS classes, and ARIA labels to the form fields.

6. `OptionForm`
   The `OptionForm` is used for creating and editing options. It is associated with the `Option` model and customizes the widget for the 'name' and 'statement' fields. These fields have placeholders, CSS classes, and ARIA labels for a better user interface.

7. `QuotationForm`
   The `QuotationForm` is designed for creating and editing quotations. It is associated with the `Quotation` model and provides extensive customization for various fields. These customizations include input styling, CSS classes, and ARIA labels for fields like price, time, unit, document requirements, and more. Additionally, it handles file uploads for quotation formats.

8. `NextActivitiesOnQuotation`
   The `NextActivitiesOnQuotation` form is intended for updating next activities on quotations. It is associated with the `Quotation` model and customizes the widget for the 'next_activities' field with styling and a select input.

9. `SuggestionForm`
   The `SuggestionForm` allows the creation and editing of suggestions. It is associated with the `Suggestions` model and provides customization for fields like suggestion type, title, and statement. The form includes select inputs, text inputs, and text areas with appropriate attributes to enhance user interaction.

10. `QuesSugestionForm`
   The `QuesSugestionForm` is a custom form for creating and editing question suggestions. It is associated with the `Suggestions` model and includes a special constructor (`__init__`) that populates choices for the 'related_qs' field based on a custom function. The form also customizes the widget for 'su_type,' 'title,' 'statement,' and 'related_qs' fields. It provides select inputs, text inputs, and text areas, along with appropriate placeholders and attributes. This form enhances the user experience in creating and editing question suggestions.

11. `NextActivitiesForm`
   The `NextActivitiesForm` is used for creating and editing next activities. It is associated with the `NextActivities` model and includes a constructor to handle the 'request' object. The form customizes the widget for various fields, including 'related_questions,' 'compulsory_questions,' 'name_and_standared,' 'priority,' and others. It provides input styling, placeholders, and attributes for an improved user experience. The form also includes a custom `save` method that checks for the existence of instances with the same selected IDs and, if found, takes specific actions such as updating user IDs and sending notifications to the admin.


## helper.py

The `helper.py` module contains a set of custom helper methods aimed at assisting with data calculation and retrieval. These methods offer valuable functionality for calculating the total number of reports, the total number of reports created by the current user, and counting the number of users under each label.

1. `total_reports(request)`
   The `total_reports` method calculates the total number of reports in the database. It queries the `Evaluator` model and counts all instances. This count is useful for generating statistics and insights regarding the reports within your application.

2. `total_this_user_report(request)`
   The `total_this_user_report` method calculates the total number of reports created by the current user. It filters the `Evaluator` model by the creator attribute, which is set to the current user, and counts the instances. This count helps users monitor and manage their own reports.

3. `users_under_each_label(request)`
   The `users_under_each_label` method counts the number of users associated with each label. It retrieves a list of labels by calling `get_all_definedlabel()` and filters out labels marked as common. To optimize database queries, it prefetches related users for each label. The method constructs a dictionary where the keys represent label names, and the values indicate the count of users under each label. This information is valuable for analyzing user distribution based on labels.

4. `reports_under_each_biofuel(request)`
   The `reports_under_each_biofuel` method counts the number of reports under each biofuel category. It retrieves the biofuel categories and calculates the count of reports associated with each category. The results are stored in a dictionary where the keys represent biofuel names, and the values represent the count of reports under each biofuel category. This information is valuable for understanding the distribution of reports based on biofuel types.

5. `weeks_results(request)`
   The `weeks_results` method retrieves the number of reports generated in the last year and formats the results. It calculates the date one year ago from the current date, filters reports created in the last year, and aggregates the report counts by month/year. The results are formatted into a dictionary where keys are formatted date strings (month/year), and values represent the report counts. This information is useful for tracking report generation trends over time.

6. `all_reports(request)`
   The `all_reports` method retrieves and filters reports based on user roles and calculates additional statistics. It checks the user's role, and if they are a staff member or superuser, all reports are shown. For regular users, only their reports are displayed. The method calculates the number of answered, positive, and "don't know" responses for each report, providing insights into response patterns. The results are paginated, with 10 reports per page, and additional statistics are included in each report's information. This method streamlines report management, making it easier to access and analyze data.

7. `typewise_user(request)`
    The `typewise_user` method fetches all user types, each of which represents a specific classification or role for users in your application. To optimize database queries, it prefetches related users for each user type. The method returns a dictionary where the keys are user type objects, and the values are lists of associated users, limited to the first 4 users for each type. This limitation helps provide a concise overview of user types and their members.

This method is beneficial for various purposes, including generating user statistics, understanding user role distributions, and facilitating user management.
These helper methods simplify data processing and statistics generation within your application. Developers can leverage these methods in various scenarios, such as generating reports, user management, or label-based analytics. Integration into your views or other application components is essential to maximize the benefits of these methods.

For detailed information on using these methods and their integration into your Django project, please refer to the associated views and templates in your application. These methods serve as essential components for data analysis and user management.



## models.py

This section of `models.py` introduces several essential models designed to represent various attributes within the application, such as price units, time units, weight units, and quotation document types. These models serve as fundamental components for managing and categorizing data. Here's a detailed explanation:

1. `User` Model
   The `User` model is dynamically defined based on the project's `AUTH_USER_MODEL` setting. It represents the user entities within your application. This model stores user-related information and is used for user authentication and management. The specific fields and attributes associated with the `User` model are determined by your project's settings.

2. `PriceUnit` Model
   The `PriceUnit` model represents different price units used in the application, such as currency symbols (e.g., USD, EUR). Each instance of this model corresponds to a specific price unit. The `name` attribute stores the name of the price unit. This model simplifies the handling of price-related data.

3. `TimeUnit` Model
   The `TimeUnit` model represents time units, such as minutes and hours. Each instance of this model corresponds to a specific time unit. The `name` attribute stores the name of the time unit. This model is valuable for dealing with time-related calculations and data presentation.

4. `WeightUnit` Model
   The `WeightUnit` model represents various weight units, such as kilograms (kg) and pounds (lb). Each instance of this model corresponds to a specific weight unit. The `name` attribute stores the name of the weight unit. This model simplifies the handling of weight-related data.

5. `QuotationDocType` Model
   The `QuotationDocType` model represents different document types that can be associated with quotations. Examples of document types include PDF and Word documents. Each instance of this model corresponds to a specific document type. The `name` attribute stores the name of the document type. This model categorizes and manages document types associated with quotations.

6. `Quotation` Model
   The `Quotation` model represents a quotation for testing services. It stores essential information related to the quotation and is used to manage quotations provided by service providers. Below are the attributes and their descriptions associated with the `Quotation` model:

   1. `service_provider` (ForeignKey to User)
      - Represents the user who provides the quotation.
      
   2. `show_alternate_email` (EmailField, optional)
      - Represents an alternate email address for the quotation (optional).

   3. `show_alternate_business` (CharField, optional)
      - Represents an alternate business name for the quotation (optional).

   4. `show_alternate_phone` (CharField, optional)
      - Represents an alternate phone number for the quotation (optional).

   5. `price` (DecimalField)
      - Stores the quotation's price. Users should provide the price for the service.

   6. `price_unit` (ForeignKey to PriceUnit)
      - Represents the unit of the price. Users can choose from available pricing units.

   7. `needy_time` (IntegerField)
      - Indicates the time needed for the test to be conducted.

   8. `needy_time_unit` (ForeignKey to TimeUnit)
      - Represents the unit of time needed for the test.

   9. `sample_amount` (IntegerField)
      - Stores the amount of sample needed for the test.

   10. `sample_amount_unit` (ForeignKey to WeightUnit)
       - Represents the unit of weight for the sample amount.

   11. `require_documents` (ManyToManyField to QuotationDocType)
       - Represents the documents needed for the test. Users can select multiple document types required for the service.

   12. `factory_pickup` (BooleanField)
       - Indicates whether the sample will be collected from the factory.

   13. `test_for` (ForeignKey to Question)
       - Represents the question for which the test is conducted. Users can select from available questions.

   14. `related_questions` (ManyToManyField to Question)
       - Allows the selection of other questions that are tested within the provided quotation. Users can select multiple related questions.

   15. `quotation_format` (FileField)
       - Allows the uploading of a quotation file, which must be in PDF format.

   16. `next_activities` (ForeignKey to NextActivities, optional)
       - Represents next activities related to the quotation (optional).

   17. `display_site_address` (BooleanField)
       - Indicates if the site address should be displayed.

   18. `comments` (TextField, optional)
       - Provides an additional space for users to add comments related to the quotation (optional).

   Key Properties and Methods:
   - `get_quot_url`: Returns the URL to add a new quotation for the corresponding question.
   - `get_business_name`: Retrieves the business name for the quotation based on display settings.
   - `get_phone`: Retrieves the phone number for the quotation based on display settings.
   - `get_email`: Retrieves the email address for the quotation based on display settings.
   - `get_absolute_url`: Gets the absolute URL for the quotation report.

The `Quotation` model is a fundamental component of your application for managing quotations for testing services, facilitating interactions between service providers and users seeking testing services.

These models are vital for maintaining consistent and organized data storage within your application. Developers can create, update, and retrieve instances of these models as needed to manage and categorize various attributes and data types effectively.

For detailed information on using these models, including creating and managing instances, refer to the relevant views, forms, and templates in your application. These models serve as the foundation for data representation and management.


## views.py

This document provides an overview of the views defined in the project's `views.py` file. Views are responsible for handling HTTP requests and returning appropriate HTTP responses. Below are the main views and their descriptions:

1. `home(request)`
   - View for the home page.
   - Displays information on the home page.
   - Caches user types and latest blog posts for efficient access.
   - Meta data is set for page details.
   - Available context data:
     - `user_types`: Cached user types.
     - `latest_blogs`: Cached latest blog posts.
     - `site_info`: Meta data for the page.

2. `user_types(request, slug)`
   - View for displaying different user types and initiating the user signup journey.
   - Sets the 'interested_in' session variable to the selected user type's slug.
   - Ensures the user is logged in to initiate enrollment.
   - Determines enrollment options based on user type and permissions.
   - Retrieves user type data and related users.
   - Meta data is set for page details.
   - Available context data:
     - `user_type`: Selected user type.
     - `users`: Users associated with the selected user type.
     - `enroll`: Enrollment options.
     - `site_info`: Meta data for the page.

3. `dashboard(request)`
   - View for displaying the user dashboard.
   - Requires the user to be logged in.
   - Provides a summary of dashboard data, including weekly results, user labels, biofuel records, and more.
   - Meta data is set for page details.
   - Available context data:
     - `user_of_labels`: User labels statistics.
     - `biofuel_records`: Biofuel records statistics.
     - `day_of_week`: Days of the week for weekly results.
     - `total_of_day`: Total reports for each day of the week.
     - `total_reports`: Total number of reports.
     - `allreports`: Paginated list of reports and additional statistics.
     - `typewise_user`: User types and associated users.
     - `site_info`: Meta data for the page.


4. `questionsint(request)`
   - View for displaying questions related to the current marine user.
   - Protected with `@login_required` and `@marine_required` decorators, ensuring that only logged-in marine users can access it.
   - Provides specialized questions to get feedback from marine experts.
   - Retrieves parent questions and related child questions.
   - Paginates the results for display.
   - Meta data is set for page details.
   - Available context data:
     - `questions`: Specialized questions for marine users.
     - `site_info`: Meta data for the page.

5. `user_setting(request)`
   - View for managing user settings and profile.
   - Allows logged-in users to update their general information, profile data, password, company logo, and notification settings.
   - Handles different form submissions for various sections of user settings.
   - Initializes form instances for different sections.
   - Meta data is set for page details.
   - Available context data:
     - `user`: The logged-in user.
     - `user_form`: Form for general user information.
     - `profile_form`: Form for user profile data.
     - `password_form`: Form for changing the password.
     - `company_logo_form`: Form for updating the company logo.
     - `notification_form`: Form for notification settings.
     - `site_info`: Meta data for the page.

6. `delete_avatar(request)`
   - View for deleting the user's avatar.
   - Deletes the user's company logo from the profile.
   - Redirects to the user settings page after deletion.

7. `password_change(request)`
   - View for changing the user's password.
   - Allows logged-in users to change their password by providing the current and new password.
   - Handles form submissions for changing the password.
   - Initializes the form instance for changing the password.
   - Updates the session auth hash after password change.
   - Meta data is set for page details.
   - Available context data:
     - `user`: The logged-in user.
     - `password_form`: Form for changing the password.
     - `site_info`: Meta data for the page.

8. `get_question_of_label(request)`
   - View to retrieve questions of a specific label.
   - Checks if the user has the necessary permissions (staff, superuser, expert, marine) to access questions.
   - If the user has the required permissions, it retrieves all questions.
   - If the user lacks permissions, it redirects and displays a warning message.
   - Available context data:
     - `questions`: A list of questions (or a redirection if user lacks permissions).

9. `child_modal_data(request, id)`
   - View to retrieve data for a child question modal.
   - Designed to fetch data for a child question modal.
   - Checks if the user is logged in, returning a message if not.
   - Ensures access is allowed to experts only, returning a message if the user lacks the necessary permissions.
   - Retrieves the question data with related data prefetching.
   - Renders a child question modal data template.
   - Available context data:
     - `qquestion`: Question data.


10. `quotations(request)`
    - View to display quotations related to questions.
    - Allows logged-in experts (staff, superuser) to access quotations associated with questions.
    - Retrieves questions and their related data, including quotations.
    - Provides a paginated response for viewing.
    - Meta data is set for page details.
    - Available context data:
      - `questions`: Paginated list of questions with related quotations.
      - `site_info`: Meta data for the page.

11. `quotationsatg(request)`
    - View to display quotations at a glance.
    - Allows logged-in experts (staff, superuser) to access quotations at a glance.
    - Quotations can be accessed by staff, superusers, or the service provider (user) who created them.
    - Retrieves quotations and provides a paginated response for viewing.
    - Meta data is set for page details.
    - Available context data:
      - `quotations`: Paginated list of quotations.
      - `site_info`: Meta data for the page.

12. `add_quatation(request, slug)`
    - View to add or edit a quotation for a specific question.
    - Available to logged-in experts (staff, superuser).
    - Checks if the user is logged in, has the necessary permissions, and allows adding or editing quotations.
    - Manages form submissions for adding/editing quotations.
    - Saves the quotations, related questions, and next activities.
    - Checks and validates data related to quotations.
    - Deletes the session of next activities after saving the quotation.
    - Ensures that a question exists for adding/editing quotations.
    - Meta data is set for page details.
    - Available context data:
      - `question`: The specific question for which the quotation is added or edited.
      - `form`: Form for adding/editing quotations.
      - `na_form`: Form for selecting next activities.
      - `quatation`: The quotation being added/edited.
      - `report_link`: Link to view the quotation report.
      - `site_info`: Meta data for the page.

13. `get_verbose_name(instance, field_name)`
    - Helper function to get the `verbose_name` for a field in a model instance.
    - Takes the model instance and the field name as arguments.
    - Returns the `verbose_name` of the specified field title-cased.
    
14. `quotation_report2(request, quotation_data)`
    - Sub-function to generate a PDF report based on quotation data.
    - Generates a PDF report for a given quotation data.
    - Creates a PDF document using the ReportLab library and includes quotation details, related questions, and additional information.
    - Returns the generated PDF as a BytesIO buffer.
    
15. `quotation_report(request, question, quotation)`
    - View to return a final report with an attachment as a PDF.
    - Generates a final report in PDF format by merging the contents of a quotation report and an attachment (if available) into a single PDF document.
    - Uses the PyPDF2 library to merge the two PDFs.
    - Returns the generated PDF report as an HTTP response.
    - Available context data:
      - `question`: The question associated with the quotation.
      - `quotation`: The ID of the quotation for which the report is generated.

16. `questions_details(request, slug)`
    - View to display and edit the details of a specific question.
    - Marine experts can view and edit the question text, associated options, and other attributes.
    - The view uses a combined form that includes the main question and its associated options.
    - Available context data:
      - `slug`: The slug of the question to be displayed and edited.
      - `question`: The specific question to be edited.
    - Returns an HTTP response containing the question details and an editable form.

17. `new_questions(request)`
    - View to add a new question and associated options.
    - Marine experts can add a new question along with its associated options.
    - The view provides a form for inputting the question text and options for the new question.
    - Available context data:
      - No specific context data other than site metadata.
    - Returns an HTTP response containing the form for adding a new question and options.

18. `allreports(request)`
    - View to display a list of evaluation reports for biofuels.
    - Admin users can see all reports, while biofuel producers can only see their own reports.
    - The view provides a list of evaluation reports for biofuels.
    - Available context data:
      - No specific context data other than site metadata.
    - Returns an HTTP response containing the list of evaluation reports.

19. `check_type_to_get_expert(request)`
    - View to check the user type selected during registration and set session variables accordingly.
    - Used during the registration process to determine the user type selected by the user and set session variables based on that selection.
    - Retrieves the user type from the request's POST data and sets the 'interested_in' session variable to the user type's slug.
    - Sets the 'hidden' session variable to 'hidden' if the user type is not an expert, indicating that certain form fields should be hidden in the registration form.
    - Returns a redirection to the registration page.

20. `add_extra(request, pk)`
    - View to add an extra form field.
    - Increments the 'extra' session variable to control front-end behavior.
    - Returns a redirection to the question details page.

21. `sub_extra(request, pk)`
    - View to subtract an extra form field.
    - Decrements the 'extra' session variable if it's greater than or equal to 1 to control front-end behavior.
    - Returns a redirection to the question details page.

22. `webmanifest(request)`
    - View to generate a web app manifest.
    - Creates a web app manifest containing data such as the app's name, icons, and other configuration options.
    - Returns a JSON response containing the web app manifest data.
    
23. `AddSugestion(View)`
    - Class-based view for adding or editing suggestions related to a question.
    - Handles both GET and POST requests for displaying the form and processing form submissions.
    - Attributes:
        - `get_temp` (str): Template file for rendering the form.
        - `form_class` (class): Form class used for suggestion input.
    - Methods:
        - `get(self, request, *args, **kwargs)`: Handles GET requests to display the suggestion form.
        - `post(self, request, *args, **kwargs)`: Handles POST requests to process form submissions.

24. `get_edit_sugestion(request, slug, pk)`
    - View to edit an existing suggestion related to a question.
    - Allows marine users to edit an existing suggestion for a specific question based on its primary key (pk).

25. `get_sugestion_list(request, slug)`
    - View to display a list of suggestions related to a specific question.
    - Retrieves and displays a list of suggestions related to a specific question, identified by its slug.

26. `delete_sugestion(request, pk)`
    - View to delete a suggestion.
    - Allows authenticated users, typically marine experts, to delete a specific suggestion based on its primary key (pk).
    - Users must have the necessary permissions to delete the suggestion. Only the creator of the suggestion, admin users, and superusers can delete it.

27. `sugest_new_ques_option(request)`
    - View to suggest new questions and options for evaluation.
    - Allows marine experts to submit suggestions for new questions and corresponding options.
    - The submitted suggestions are reviewed and, if approved, added to the evaluation pool.
    - Displays previously suggested questions by the same expert.
    
28. `get_edit_new_sugestion(request, pk)`
    - View to edit a new suggestion.
    - Allows marine experts to edit a previously suggested question or option.
    - Experts can update the statement, title, related questions, and suggestion type.
    - Changes are saved if the expert is the creator of the suggestion or has staff/superuser privileges.
    
29. `get_new_sugestion_list(request)`
    - View to display a list of new suggestions created by the marine expert.
    - Retrieves and displays a list of new suggestions created by the marine expert.
    - These suggestions have not been associated with a specific question or option yet.
    

30. `add_new_service(request, user_id)`
    - View to allow an expert to add a new service or select an existing service for a visiting user.
    - Allows an expert user to add a new service or select an existing service for a visiting user.
    - The expert can provide details about the service and associate it with related and compulsory questions.
    - If an existing service is found for the selected questions, the expert is prompted to select that service.

These views empower expert users to provide services and options to visiting users and facilitate the management of services associated with specific questions.

Please note that these views are part of the project's features for user interaction and service management. Additional views and features may be defined elsewhere in the project based on specific requirements.

These views serve as the core components of the project, handling various functionalities and interactions with users on the website.

Please note that the mentioned views are not the entire list of views in the project. Additional views may be defined elsewhere in the project based on specific requirements.



## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.



## Credits

This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).

