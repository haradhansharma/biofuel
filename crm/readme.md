=============================
Django CRM App - admin.py
=============================

Introduction
------------

Welcome to the Django CRM App! This README provides an overview of the `admin.py` file, explaining its role within the project. The `admin.py` file is an essential part of the app's functionality, as it customizes the Django admin interface for specific models.

Purpose
-------

The `admin.py` File:
~~~~~~~~~~~~~~~~~~~~

The `admin.py` file in this app is responsible for configuring how certain models are displayed and managed within the Django admin panel. It leverages the Django admin site framework to provide an intuitive and user-friendly way for administrators to interact with the app's data.

Contents
--------

The `admin.py` file contains the following sections:

1. Model Registrations: The file uses the `admin.site.register()` function and decorator-based registration (`@admin.register(ModelName)`) to associate specific models with the admin site.

2. Custom Admin Classes: Two custom admin classes, `MailQueueAdmin` and `BlogMailQueueAdmin`, are defined. These classes inherit from `admin.ModelAdmin` and customize the presentation and behavior of their respective models within the admin interface.

3. `list_display` Attribute: Both custom admin classes define a `list_display` attribute. This attribute determines which fields of the model are shown in the list view of the admin interface.

Usage
-----

To add or modify the behavior of models in the Django admin panel:

1. Open the `admin.py` file located in your CRM app's directory.

2. Locate the relevant model's admin class or create a new one if needed.

3. Customize the `list_display` attribute to specify which fields should appear in the list view of the admin interface.

4. Utilize other attributes and methods available in `admin.ModelAdmin` to further tailor the admin panel's behavior to your needs.




The `forms.py` File:
===================

The `forms.py` file is responsible for defining custom form classes that facilitate user interactions with the Django CRM App. These forms are designed to collect and process data submitted by users through the app's interface.

Contents
--------

The `forms.py` file contains the following form classes:

1. `UploadLead` Form:
   - Purpose: Allows users to upload lead data as a file.
   - Form Field: `lead_upload` (FileField) for handling file uploads.
   - Usage: Users can submit lead data files for processing within the app.

2. `SubscriberForm` Form:
   - Purpose: Collects information from users who wish to subscribe.
   - Form Fields: `name` (CharField) for the subscriber's name, and `email` (EmailField) for the subscriber's email.
   - Usage: Users can provide their name and email to subscribe to updates from the app.

Usage
-----

To utilize the forms defined in `forms.py` within your Django CRM App:

1. Open the `forms.py` file located in your app's directory.

2. Review the available form classes, such as `UploadLead` and `SubscriberForm`.

3. Integrate the desired form into your app's views or templates as needed.

4. Leverage the fields and attributes provided by each form class to customize the form's appearance and behavior.


The `lead_mail_jobs.py` File:
============

Lead CRM App is a Django application designed to help manage customer leads and streamline email communication.


Usage
-----

### Email Queue Functions

The `lead_mail_jobs.py` module provides several functions related to email queue management. These functions can be useful for handling email communication within your CRM app.

1. `last_process_time()`

    Returns the time of the most recent email processing.

    ```python
    from lead_mail_jobs import last_process_time

    last_time = last_process_time()
    if last_time:
        print("Last email processing time:", last_time)
    ```

2. `total_mail_sent()`

    Returns the total number of emails that have been processed.

    ```python
    from lead_mail_jobs import total_mail_sent

    total_sent = total_mail_sent()
    print("Total emails sent:", total_sent)
    ```

3. `pending_queue_count()`

    Returns the number of emails pending in the queue.

    ```python
    from lead_mail_jobs import pending_queue_count

    pending_count = pending_queue_count()
    print("Pending emails in the queue:", pending_count)
    ```

4. `send_custom_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None)`

    Sends a batch of custom HTML emails using the provided data.

    Args:
      - `datatuple`: A list of tuples where each tuple contains subject, message, sender, and recipient information.
      - `fail_silently`: If `True`, exceptions during sending will be suppressed. Default is `False`.
      - `auth_user`: The username for email server authentication. Default is `None`.
      - `auth_password`: The password for email server authentication. Default is `None`.
      - `connection`: An existing email connection. If not provided, a new connection will be created.

    Returns:
      - `int`: The number of successfully sent emails.

    ```python
    from lead_mail_jobs import send_custom_mass_mail

    email_data = [
        ("Subject 1", "<html><body>Message 1</body></html>", "sender@example.com", "recipient1@example.com"),
        ("Subject 2", "<html><body>Message 2</body></html>", "sender@example.com", "recipient2@example.com"),
        # ...
    ]

    sent_count = send_custom_mass_mail(email_data)
    print("Total emails sent:", sent_count)
    ```

### Sending Lead Emails

The `send_lead_mail()` function in the `lead_mail_jobs.py` module is responsible for sending lead emails from the queue within the Lead CRM App.

#### Function Overview

This function performs the following tasks:

1. Checks if it's time to send lead emails based on the last execution time.
2. Retrieves a batch of pending emails from the `MailQueue` table.
3. Constructs personalized email messages for each lead.
4. Sends the emails in bulk to the corresponding recipients.
5. Updates the queue for processed emails and handles problematic cases.
6. Deletes emails that have been tried more than twice or are older than 90 days.

#### Usage Example

To use the `send_lead_mail()` function, follow these steps:

1. Ensure you have imported necessary modules and models:

    ```python
    from lead_mail_jobs import send_lead_mail
    from lead.models import Lead, MailQueue
    from django.contrib.sites.models import Site
    from django.template.loader import render_to_string
    from django.utils import timezone
    from django.utils.safestring import mark_safe
    from django.conf import settings
    import logging
    ```

2. Call the `send_lead_mail()` function:

    ```python
    total_sent = send_lead_mail()
    print(f"Total lead emails sent: {total_sent}")
    ```

#### Configuration and Customization

Before using the `send_lead_mail()` function, ensure you have the following set up correctly:

- Make sure your `settings.py` includes configurations for email sending, such as `DEFAULT_FROM_EMAIL`.
- Adjust the `LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME` setting to control the number of emails sent in a batch.
- Customize the email content by modifying the template file `emails/crm_initial_mail.html`.
- Customize the subject line of the emails by modifying the `subject` variable.

#### Cleanup and Error Handling

The function handles cases where emails fail to send, and it removes emails from the queue if they have been tried more than twice or are older than 90 days.

For any errors or exceptions encountered during the process, the function logs them using the `logging` module, ensuring you have appropriate logging configured.

Remember to set up proper error handling and logging mechanisms in your project to handle unexpected scenarios.

---

Feel free to adapt and integrate the `send_lead_mail()` function to your CRM app's requirements and workflows. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.


### Sending Blog-related Emails

The `send_blog_mail()` function within the `lead_mail_jobs.py` module is responsible for sending blog-related emails from the queue within the Lead CRM App.

#### Function Overview

This function handles the process of sending personalized emails to recipients based on blog posts. It performs the following tasks:

1. Checks if it's time to send blog-related emails based on the last execution time.
2. Retrieves a batch of pending emails from the `BlogMailQueue` table.
3. Constructs personalized email messages for each recipient using blog post information.
4. Sends the emails in bulk to the corresponding recipients.
5. Updates the queue for processed emails and handles problematic cases.
6. Deletes emails that have been tried more than twice or are older than 90 days.

#### Usage Example

To utilize the `send_blog_mail()` function, follow these steps:

1. Ensure you have the necessary imports at the beginning of your script:

    ```python
    from lead_mail_jobs import send_blog_mail
    from lead.models import Lead, BlogMailQueue, BlogPost
    from lead.utils import site_info
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.utils import timezone
    from django.utils.safestring import mark_safe
    from django.conf import settings
    from django.db.models import Count
    import logging
    ```

2. Call the `send_blog_mail()` function:

    ```python
    total_sent = send_blog_mail()
    print(f"Total blog-related emails sent: {total_sent}")
    ```

#### Configuration and Customization

Before using the `send_blog_mail()` function, ensure you have the following configured correctly:

- Make sure your `settings.py` includes configurations for email sending, such as `DEFAULT_FROM_EMAIL`.
- Adjust the `LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME` setting to control the number of emails sent in a batch.
- Customize the email content by modifying the template file `emails/crm_blog_mail.html`.
- Customize the subject line of the emails by modifying the `subject` variable.
- Adjust the logic inside the function to match your application's specific requirements.

#### Cleanup and Error Handling

The function handles cases where emails fail to send and removes emails from the queue if they have been tried more than twice or are older than 90 days.

For any errors or exceptions encountered during the process, the function logs them using the `logging` module, ensuring you have appropriate logging configured.

Remember to set up proper error handling and logging mechanisms in your project to handle unexpected scenarios.

---

Feel free to adapt and integrate the `send_blog_mail()` function into your CRM app as needed. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.



### Sending Report-related Emails

The `send_report_queue()` function within the `lead_mail_jobs.py` module is responsible for sending report-related emails from the queue within the Lead CRM App.

#### Function Overview

This function handles the process of sending personalized emails to recipients based on report updates. It performs the following tasks:

1. Checks if it's time to send report-related emails based on the last execution time.
2. Retrieves a batch of pending emails from the `ReportMailQueue` table.
3. Constructs personalized email messages for each recipient using report update information.
4. Sends the emails in bulk to the corresponding recipients.
5. Updates the queue for processed emails and handles problematic cases.
6. Deletes emails that have been tried more than twice or are older than 90 days.

#### Usage Example

To utilize the `send_report_queue()` function, follow these steps:

1. Ensure you have the necessary imports at the beginning of your script:

    ```python
    from lead_mail_jobs import send_report_queue
    from lead.models import ReportMailQueue
    from lead.utils import site_info
    from django.template.loader import render_to_string
    from django.utils import timezone
    from django.utils.safestring import mark_safe
    from django.conf import settings
    import logging
    ```

2. Call the `send_report_queue()` function:

    ```python
    total_sent = send_report_queue()
    print(f"Total report-related emails sent: {total_sent}")
    ```

#### Configuration and Customization

Before using the `send_report_queue()` function, ensure you have the following configured correctly:

- Make sure your `settings.py` includes configurations for email sending, such as `DEFAULT_FROM_EMAIL`.
- Adjust the `LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME` setting to control the number of emails sent in a batch.
- Customize the email content by modifying the template file `emails/feedback_update.html`.
- Adjust the logic inside the function to match your application's specific requirements.

#### Cleanup and Error Handling

The function handles cases where emails fail to send and removes emails from the queue if they have been tried more than twice or are older than 90 days.

For any errors or exceptions encountered during the process, the function logs them using the `logging` module, ensuring you have appropriate logging configured.

Remember to set up proper error handling and logging mechanisms in your project to handle unexpected scenarios.

---

Feel free to adapt and integrate the `send_report_queue()` function into your CRM app as needed. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.

Sending New Fuel Report Notifications
=====================================

The `send_new_report_notification()` function is responsible for sending notifications to consumers for new fuel reports within the Lead CRM App.

#### Function Overview

This function handles the process of sending personalized email notifications to consumers based on new fuel report submissions. It performs the following tasks:

1. Retrieves a batch of pending email notifications from the `ConsumerMailQueue` table.
2. Constructs personalized notification messages for each recipient with information about the new fuel report.
3. Sends the notification emails in bulk to the corresponding recipients.
4. Updates the queue for processed notifications and handles cases where emails fail to send.
5. Deletes old queue entries that have been tried more than twice or are older than 90 days.

#### Usage Example

To utilize the `send_new_report_notification()` function, follow these steps:

1. Ensure you have the necessary imports at the beginning of your script:

    ```python
    from lead.models import ConsumerMailQueue
    from lead.utils import site_info, build_full_url
    from django.utils import timezone
    from django.conf import settings
    import logging
    from django.db.models import Q
    from lead.utils import send_custom_mass_mail
    ```

2. Call the `send_new_report_notification()` function:

    ```python
    total_sent = send_new_report_notification()
    print(f"Total new fuel report notifications sent: {total_sent}")
    ```

#### Configuration and Customization

Before using the `send_new_report_notification()` function, ensure you have the following configured correctly:

- Make sure your `settings.py` includes configurations for email sending, such as `DEFAULT_FROM_EMAIL`.
- Adjust the `LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME` setting to control the number of notifications sent in a batch.
- Customize the notification content within the function as needed.
- Adjust the logic inside the function to match your application's specific requirements.

#### Cleanup and Error Handling

The function handles cases where notifications fail to send and removes notifications from the queue if they have been tried more than twice or are older than 90 days.

For any errors or exceptions encountered during the process, the function logs them using the `logging` module, ensuring you have appropriate logging configured.

Remember to set up proper error handling and logging mechanisms in your project to handle unexpected scenarios.
---


### Sending Queued Mails in Bulk using Cron Job

The `SendQueueMail` class extends the `CronJobBase` class from Django's `django_cron` module. This cron job is responsible for sending various types of queued mails in bulk at scheduled intervals.

#### Cron Job Overview

The `SendQueueMail` cron job handles the bulk sending of different types of queued mails, including lead mails, blog mails, and report mails. It ensures that queued mails are efficiently dispatched to their recipients while minimizing load and potential issues.

#### Usage Example

To use the `SendQueueMail` cron job, follow these steps:

1. Import the necessary modules at the beginning of your script:

    ```python
    from django_cron import CronJobBase, Schedule
    from .lead_mail_jobs import send_lead_mail
    from .lead_mail_jobs import send_blog_mail
    from .lead_mail_jobs import send_report_queue
    import logging
    ```

2. Define your `SendQueueMail` class, ensuring it extends `CronJobBase`:

    ```python
    class SendQueueMail(CronJobBase):
        RUN_EVERY_MINS = 5
        RETRY_AFTER_FAILURE_MINS = 1
        MIN_NUM_FAILURES = 2    
        ALLOW_PARALLEL_RUNS = True
        schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
        code = 'crm.send_queue_mail'
        
        def do(self):
            try:
                # Send lead mails
                total_lead_mails_sent = send_lead_mail()
                log.info(f'{total_lead_mails_sent} lead mail(s) have been sent')
                
                # Send blog mails
                total_blog_mails_sent = send_blog_mail()
                log.info(f'{total_blog_mails_sent} blog mail(s) have been sent')
                
                # Send report mails
                total_report_mails_sent = send_report_queue()
                log.info(f'{total_report_mails_sent} report mail(s) have been sent')

                # Send new report mails to consumer
               total_consumer_mail_sent = send_new_report_notification()
               log.info(f'{total_consumer_mail_sent} report mail(s) have been sent')
            
            except Exception as e:
                log.exception(f'An error occurred while sending queued mails: {e}')
    ```

3. Ensure you have the required logging configured to handle exceptions and logs effectively.

#### Configuration and Customization

The `SendQueueMail` cron job class can be customized to suit your application's requirements. You can adjust the `RUN_EVERY_MINS` value to set the frequency of the cron job execution. Additionally, you can modify the `do()` method to include any other types of queued mails or additional processing logic.

#### Error Handling

The cron job employs robust error handling mechanisms. In case of any exceptions during the execution of the cron job, it logs the error and provides details for troubleshooting.

---

Feel free to incorporate the `SendQueueMail` cron job class into your CRM app's workflow to ensure efficient and timely delivery of queued mails. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.



### Sending New Report Notifications

The `send_new_report_notification()` function within the `your_module.py` module is responsible for sending notifications to consumers about new fuel reports within your application.

#### Function Overview

This function retrieves pending email notifications from the queue, constructs notification messages, and sends them to consumers. It also handles updating the queue and deleting old queue entries. Here's a brief overview of what it does:

1. **Retrieve Pending Emails**: The function fetches pending email notifications from the queue that haven't been processed yet.

2. **Construct Messages**: It constructs individual notification messages for each pending email, including information about the new fuel report and a link to it.

3. **Update Queue**: The function updates the pending email records by incrementing the "tried" count, marking them as processed, and recording the process time.

4. **Send Emails**: It sends the constructed notification emails to the respective consumers.

5. **Delete Old Entries**: The function identifies and deletes old queue entries that meet specific conditions (e.g., tried more than twice or older than 90 days).

#### Usage

You can call this function as needed within your Django project, typically as part of a scheduled task using Django's built-in cron-like scheduler or a third-party package like `django-cron`. It helps ensure that consumers are notified about new fuel reports efficiently.

```python
from your_module import send_new_report_notification

# Call the function to send new report notifications
total_sent = send_new_report_notification()

----



### Deleting Incomplete Reports using Cron Job

The `DeleteIncompleteReports` class extends the `CronJobBase` class from Django's `django_cron` module. This cron job is responsible for periodically deleting incomplete reports from the system.

#### Cron Job Overview

The `DeleteIncompleteReports` cron job ensures that incomplete reports are regularly cleaned up from the system to maintain data accuracy and prevent unnecessary clutter. It uses the `clear_evaluator` utility function to identify and remove incomplete reports.

#### Usage Example

To use the `DeleteIncompleteReports` cron job, follow these steps:

1. Import the necessary modules at the beginning of your script:

    ```python
    from django_cron import CronJobBase, Schedule
    from .report_utilities import clear_evaluator  # Import the appropriate utility function
    import logging
    ```

2. Define your `DeleteIncompleteReports` class, ensuring it extends `CronJobBase`:

    ```python
    class DeleteIncompleteReports(CronJobBase):
        RUN_EVERY_MINS = 5
        RETRY_AFTER_FAILURE_MINS = 1
        MIN_NUM_FAILURES = 2    
        ALLOW_PARALLEL_RUNS = True
        schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
        code = 'crm.delete_incomplete_reports'
        
        def do(self):
            try:
                deleted_count = clear_evaluator()
                log.info(f'{deleted_count} incomplete report(s) have been deleted')
            except Exception as e:
                log.exception(f'An error occurred while deleting incomplete reports: {e}')
    ```

3. Ensure you have the required logging configured to handle exceptions and logs effectively.

#### Configuration and Customization

The `DeleteIncompleteReports` cron job class can be customized to suit your application's requirements. You can adjust the `RUN_EVERY_MINS` value to set the frequency of the cron job execution. Additionally, you can modify the `do()` method to include any other cleanup logic.

#### Error Handling

The cron job employs robust error handling mechanisms. In case of any exceptions during the execution of the cron job, it logs the error and provides details for troubleshooting.

---

Utilize the `DeleteIncompleteReports` cron job class to automatically maintain a clean and accurate system by regularly removing incomplete reports. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.




### URL Patterns in the CRM App

The `urls.py` file in the CRM app defines URL patterns that map specific URLs to their corresponding views. This allows users to access different parts of the CRM application through their web browser.

#### URL Patterns Overview

The URL patterns are defined using Django's `path()` function, which maps a URL to a view function. Each URL pattern has a unique identifier called the `name`, which can be used to generate URLs in templates.

#### URL Definitions

The `urls.py` file includes the following URL patterns:

1. **Leads View** (`leads`):
    - URL: `/crm/leads`
    - View: `leads` function
    - Purpose: Displays content related to leads in the CRM.

2. **Unsubscribe View** (`unsubscrib`):
    - URL: `/crm/unsubscrib/<email>/<code>`
    - View: `unsubscrib` function
    - Parameters: `email` (email address of the subscriber), `code` (unsubscribe code)
    - Purpose: Handles email unsubscription for a specific email address.

3. **Subscribe View** (`subscrib`):
    - URL: `/crm/subscrib/<str:email>`
    - View: `subscrib` function
    - Parameter: `email` (email address of the subscriber)
    - Purpose: Handles email subscription for a specific email address.

4. **Subscription View** (`subscription`):
    - URL: `/crm/subscription`
    - View: `subscription` function
    - Purpose: Displays content related to email subscription.

#### Usage Example

To access the different parts of the CRM application, users can use the defined URLs. For example:
- To view leads: `/crm/leads`
- To unsubscribe: `/crm/unsubscrib/user@example.com/abcdef123456`
- To subscribe: `/crm/subscrib/user@example.com`
- To manage subscriptions: `/crm/subscription`

#### Customization and Extension

You can customize the URL patterns to match your application's requirements. Add new URL patterns and map them to appropriate views as needed. Make sure to update the `views.py` file with the corresponding view functions.

#### URL Naming and Templates

Utilize the `name` parameter in URL patterns to generate URLs dynamically in templates using the `{% url %}` template tag. This ensures consistent and accurate URL generation throughout your application.

---

The URL patterns defined in the `urls.py` file enable users to access various features and functionalities of the CRM app. If you encounter any issues or need further assistance, refer to the documentation or reach out to the development team for support.




### Models in the CRM App

The `models.py` file in the CRM app defines the database models used to store and manage various types of data within the application. These models represent key entities and relationships in the CRM system.

#### Model Overview

The `models.py` file includes the following models:

1. **Lead Model**:
    - Represents leads in the CRM.
    - Fields: `lead`, `email_address`, `phone`, `address_1`, `address_2`, `city`, `country`, `subscribed`, `confirm_code`.
    - Purpose: Stores lead information such as name, email address, contact details, address, and subscription status.

2. **MailQueue Model**:
    - Represents queued emails in the CRM.
    - Fields: `to`, `added_at`, `processed`, `process_time`, `tried`.
    - Purpose: Stores information about emails in the queue, including recipient, timestamp, processing status, and retry count.

3. **BlogMailQueue Model**:
    - Represents queued emails related to blog posts.
    - Fields: `to`, `blog`, `added_at`, `processed`, `process_time`, `tried`.
    - Purpose: Stores information about emails in the queue related to blog posts, including recipient, associated blog post, and processing details.

#### Model Details

Each model defines its fields, data types, and relationships. The models capture important information about leads, queued emails, and blog-related emails.

#### Usage Example

To work with the models, you can use Django's Object-Relational Mapping (ORM) features. Here's an example of how you might create a new lead:

   ```python
   from crm.models import Lead

   new_lead = Lead.objects.create(
       lead='John Doe',
       email_address='john@example.com',
       phone='123-456-7890',
       city='New York',
       country='US',
       subscribed=True
   )
   ```

#### Customization and Extension

You can customize the models to match your application's requirements. Add new fields or methods to capture additional data or functionality as needed.

#### Database Synchronization

After defining or modifying models, make sure to run database migrations using the `makemigrations` and `migrate` commands to keep your database schema up-to-date.

---
The models defined in the `models.py` file enable structured storage and management of leads, queued emails, and blog-related email queues. Refer to the documentation for details on using and customizing these models, and feel free to reach out to the development team for assistance.



### Helper Function: `get_ip(request)`

The `get_ip` function in the `views.py` file is a utility function designed to retrieve the IP address of a user from an incoming HTTP request. This function is particularly useful for tracking user IP addresses in your application for various purposes, such as analytics, security, and customization.

#### Function Overview

The `get_ip` function attempts to extract the user's IP address from various headers present in the HTTP request. It prioritizes headers known to contain the real client IP address, and if none of those headers are present, it falls back to using the `REMOTE_ADDR` field from the request's `META` dictionary.

#### Function Signature

   ```python
   def get_ip(request: HttpRequest) -> str:
       """
       Get the user's IP address from the request.

       Args:
           request (HttpRequest): The HTTP request object.

       Returns:
           str: The user's IP address.
       """
   ```
#### Header Priority and Fallback
The function iterates through multiple headers, including `HTTP_X_FORWARDED_FOR`, `HTTP_CLIENT_IP`, `HTTP_X_REAL_IP`, and more, to ensure it captures the actual client IP. If none of these headers contain a valid IP, the function resorts to using the `REMOTE_ADDR` field, which typically stores the user's IP address.

#### Usage Example
You can use the `get_ip` function in your views to track and record the IP addresses of users interacting with your application. For example:

   ```python
   def my_view(request):
    user_ip = get_ip(request)
    # Process and record user IP as neededr: The user's IP address.
       """
   ```

#### Customization and Extensions
Feel free to modify the get_ip function to suit your application's specific requirements. You can add additional header checks or adapt the function to work with different proxy configurations if necessary.

---
The get_ip function simplifies the process of obtaining the user's IP address from an HTTP request, offering flexibility and ease for IP-related operations within your CRM application. Refer to the documentation for more details on its implementation and usage.




### Function: `get_location_info(request)`

The `get_location_info` function in the `views.py` file retrieves location information based on the user's IP address. This function utilizes the user's IP address, obtained through the `get_ip` function, to query the IPinfo database. The function then extracts details such as the user's city, region, country, and more.

#### Function Overview

The `get_location_info` function takes an HTTP request object as an argument. It uses the `get_ip` function to retrieve the user's IP address, and then constructs an API URL using the IP address and an API token provided in the settings. The function sends an HTTP request to the IPinfo API and processes the response JSON to extract relevant location data.

#### Function Signature

   ```python
   def get_location_info(request: HttpRequest) -> dict:
       """
       Get location information based on the user's IP address.

       Args:
           request (HttpRequest): The HTTP request object.

       Returns:
           dict: Location-related information obtained from the IPinfo database.
       """
   ```

#### API Response Handling
The function checks the HTTP response status code to ensure a successful API call (HTTP status code 200, IPINFO.io token is require). If the response code is 200, the function parses the JSON response and updates the data dictionary with location information. If the response code is not 200, the function logs an error.

#### Usage Example
You can use the get_location_info function to enhance user experiences based on their geographical location:

   ```python
   def my_view(request):
    location_data = get_location_info(request)
    # Process and utilize location data as needed
   ```

#### Customization and Extensions
The function relies on the get_ip function to retrieve IP addresses. To customize or extend functionality, consider modifying the API request URL or handling additional API response details.

---
The get_location_info function provides a convenient way to obtain user location information based on their IP address, enabling personalized experiences and insights in your CRM application. Refer to the documentation for more details on its implementation and utilization.





### Function: `subscription(request)`

The `subscription` function in the `views.py` file handles user subscription requests for newsletters. This function validates the provided name and email address, performs checks on existing subscriptions, sends confirmation emails, and returns appropriate responses to the user.

#### Function Overview

The `subscription` function takes an HTTP request object as an argument. It primarily processes POST requests containing subscription form data. The function follows these steps:
1. Validates the form data submitted by the user.
2. Checks if the provided email address already exists in the `Lead` database.
3. Sends a confirmation email for subscription or informs the user if the email is already subscribed.
4. Creates a new `Lead` entry and sends a confirmation email if the email is not found in the database.

#### Function Signature

   ```python
   def subscription(request: HttpRequest) -> HttpResponse:
       """
       Process subscription requests and send confirmation emails.

       Args:
           request (HttpRequest): The HTTP request object.

       Returns:
           HttpResponse: A response indicating the result of the subscription attempt.
       """
   ```
#### Subscription Workflow

When a user submits the subscription form, the function checks if the submitted data is valid.
1. If the email address already exists in the Lead database:
2. If the email is subscribed, an error message is returned, indicating that the email is already subscribed.
3. If the email is not subscribed, a confirmation email is sent to the user.
4. If the email address is not found in the database, a new Lead entry is created with the provided name, email address, and location information. A confirmation email is then sent.

#### Usage Example

You can use the subscription function to handle user subscription requests in your views:

   ```python
   def my_view(request):
    if request.method == 'POST':
        return subscription(request)
    else:
        # Handle GET requests or other logic
   ```

#### Customization and Extensions

This function relies on the Lead model and the SubscriberForm form for data management and validation. You can customize the email templates, modify the subscription workflow, or integrate additional functionality as per your application's requirements.

----
The subscription function streamlines the subscription process for newsletters, providing a user-friendly experience by sending confirmation emails and managing user data. Refer to the documentation for more details on its implementation and utilization.




### Function: `leads(request)`

The `leads` function in the `views.py` file handles the display and management of leads within the CRM system. It allows for lead deletion, adding leads to the mail queue for later sending, and uploading leads through a CSV file. The function also implements lead pagination and provides associated documentation.

#### Function Overview

The `leads` function requires user authentication and staff permissions to access. It processes both GET and POST requests and offers the following features:
   - Displaying and managing leads in the CRM system.
   - Deleting selected leads.
   - Adding selected leads to the mail queue for sending later.
   - Uploading leads through a CSV file.

#### Function Signature

  ```python
  @login_required
  @staff_member_required
  def leads(request: HttpRequest) -> HttpResponse:
      """
      Display and manage leads for the CRM.

      Args:
          request (HttpRequest): The HTTP request object.

      Returns:
          HttpResponse: A rendered HTML template with lead data and related information.
      """
  ```

#### Lead Management Workflow

1. Display the list of leads paginated in groups of 50 per page.
2. Process POST requests:
   
  - Delete selected leads using bulk delete.
  - Add selected leads to the mail queue for later sending.
  - Upload leads from a CSV file, processing and validating each entry.
  
   ##### Lead Management Features

     - Deleting Leads: Selecting leads and clicking the "Delete" button removes the selected leads from the CRM.
     - Adding to Mail Queue: Selecting leads and clicking the "Mail Lead" button adds them to the mail queue for later sending. Only subscribed leads are added.
     - Uploading Leads: Uploading a CSV file containing lead information adds the leads to the CRM. Errors during upload are reported.


   ##### Pagination and Meta Information

   The function uses pagination to display leads, with 50 leads per page. It also provides meta information for the page, such as title, description, tag, and robots directives.

   ##### Customization and Extensions

   This function interacts with the Lead model, supporting lead management and data storage. You can customize templates, modify lead management workflows, and integrate additional features based on your application's requirements.

----

The `leads` function offers a comprehensive interface for lead management within the CRM. It empowers users to manage leads, perform bulk actions, and upload leads through CSV files. Refer to the documentation for more details on its implementation and utilization.



Unsubscribe Function
====================

This function handles the process of unsubscribing a lead from receiving further CRM emails. When users click on the unsubscribe link sent in emails, they are directed to this view to complete the unsubscription process.

Purpose
-------
The purpose of this view is to allow users to opt-out of receiving CRM emails by unsubscribing. It verifies the provided email and confirmation code against the `Lead` model to ensure the legitimacy of the unsubscription request.

Functionality
-------------
When a user accesses the unsubscribe link with their email and confirmation code, the function performs the following steps:

1. Extracts the email and confirmation code from the URL parameters.
2. Attempts to locate a lead in the `Lead` model with the provided email and code.
3. If a valid lead is found, it sets the `subscribed` field of the lead to `False`, marking them as unsubscribed.
4. Logs the action, indicating that the lead has been successfully unsubscribed.
5. If the provided email or code is invalid, it displays a warning message and redirects the user to the home page.

Usage
-----
To unsubscribe from CRM emails, users can click on the unsubscribe link provided in the emails they receive. They will be directed to this view, where the provided email and code will be verified, and their subscription status will be updated accordingly.

Parameters
----------
- `request` (HttpRequest): The HTTP request object.
- `**kwargs`: Keyword arguments containing 'email' and 'code' from the URL.

Returns
-------
- `HttpResponse`: A rendered HTML template confirming the unsubscribed status for the lead, or an error message if the email or code is invalid.

Example
-------

  ```python
  # Unsubscribe link in email:
  # http://example.com/crm/unsubscrib/john@example.com/abc123

  # URL Parameters: email='john@example.com', code='abc123'
  def unsubscrib(request, **kwargs):
      # ... (Function implementation)
      


  ```


subscrib(request, **kwargs)
===========================

This view handles the confirmation of a lead's subscription to the CRM system. It is accessed via a confirmation link sent in subscription emails.

Arguments
---------

- ``request`` (HttpRequest): The HTTP request object.
- ``**kwargs``: Keyword arguments containing the 'email' parameter from the URL.

Functionality
-------------

When a lead clicks on the subscription confirmation link sent to their email, this function is triggered. It confirms their subscription to the CRM system by updating the 'subscribed' field of the lead's record in the database.

If the lead's email is successfully confirmed, a success template is displayed to acknowledge the subscription. If the email is not found or any errors occur, an appropriate error message is displayed.

Usage
-----

  ```python
  def subscrib(request, **kwargs):
      """
      Confirm Subscription Function
      
      This view handles the confirmation of a lead's subscription to the CRM. It is accessed via a confirmation link sent in emails.
      
      Args:
          request (HttpRequest): The HTTP request object.
          **kwargs: Keyword arguments containing 'email' from the URL.

      Returns:
          HttpResponse: A rendered HTML template confirming the subscription status for the lead or an error message if the email is invalid.
      """
      # ... (implementation details)
  ```


Contributions
-------------

If you're a developer working on this project, feel free to expand or modify the `admin.py` file to meet the evolving requirements of the CRM app. Don't forget to maintain clear code documentation, such as comments and docstrings, to help future developers understand your changes.

By working collaboratively, we can enhance the app's functionality and user experience while maintaining code quality.

For additional information or assistance, please refer to the project documentation or reach out to the development team.

Happy coding!
