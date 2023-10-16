======================================================
Django Project: GFVP (Green Fuel Validation Platform)
======================================================

Project Structure
-----------------

The 'gfvp' project has the following directory structure:

::

    gfvp/
    ├── __init__.py
    ├── settings/
    │   ├── __init__.py
    │   ├── dev.py
    │   ├── pro.py
    │   ├── settings_axes.py
    │   ├── settings_database.py
    │   ├── settings_debug_toolbar.py
    │   ├── settings_email.py
    │   ├── settings_local.py
    │   ├── settings_logs.py
    │   ├── settings_maintenance.py
    │   ├── settings_material_admin.py
    │   ├── settings_mkdocs.py
    │   ├── settings_security.py
    │   ├── settings_summernote.py
    ├── addset.cpython-39-x86_64-linux-gnu.so
    ├── addset.cp39-win_amd64.pyd
    ├── urls.py
    ├── wsgi.py
    └── asgi.py

Overview
--------

GFVP (Green Fuel Validation Platform) is a Django-based web application for managing and verifying green fuel data. It includes various features and modules for fuel evaluation, user management, content management, and more.

Getting Started
---------------

1. Install Dependencies:
   - Make sure you have Python 3.9 or higher installed.
   - Create a virtual environment and activate it.
   - Install required Python packages using ``pip install -r requirements.txt``.

2. Configure Settings:
   - Customize the project settings in the 'gfvp/settings' directory based on your environment (e.g., development or production).
   - Review 'gfvp/settings/settings_material_admin.py' for Material Admin configuration.
   - Review `CustomFileBasedCache` in project `__init__.py`

3. Database Setup:
   - Configure your database settings in 'gfvp/settings/settings_database.py'.
   - Run migrations using ``python manage.py migrate`` to create the database schema.

4. Serve the Application:
   - Start the development server with ``python manage.py runserver``.

Project Features
----------------

- Admin Panel:
  - Access the admin panel at '/admin/' with customizable branding.
  - Manage various entities and settings.

- Debugging:
  - Enable debugging using the Django Debug Toolbar at '/__debug__/'.

- Additional Modules:
  - Utilize various app modules like 'evaluation', 'home', 'crm', 'guide', 'blog', 'glossary', 'feedback', and more.

- User Management:
  - Handle user registration types with the 'null_session' view.
  - Authentication and account-related URLs are available under '/accounts/'.

- WYSIWYG Editor:
  - Integrate the Summernote WYSIWYG editor with '/summernote/'.

- Taggit Autosuggest:
  - Use the '/taggit_autosuggest/' URL for tag suggestions.

- Documentation:
  - Include documentation using MkDocs at '/docs/'.
  - Documetation for eacch app added in each app directory.

- Additional Views:
  - View GDPR policy at '/gdpr-policy/'.
  - View terms and conditions at '/terms/'.

Deployment
----------

- Configure your server for deployment.
- Set up environment variables and server-specific configurations.
- Use 'wsgi.py' (for non-Windows systems) or 'asgi.py' (for ASGI deployment) as your application entry point.
- Ensure proper permissions for cache and static/media files as required.

Contributing
------------

Feel free to contribute to this project by following our contribution guidelines and opening pull requests.

License
-------

This project is licensed under the XYZ License - see the 'LICENSE' file for details.

Acknowledgments
---------------

Special thanks to all contributors and the Django community for their support.

For more information and detailed documentation, refer to the project's official documentation.

For the latest updates and issues, visit the project repository on GitHub.

Project Repository: `https://github.com/haradhansharma/biofuel <https://github.com/harahansharma/biofuel>`_
