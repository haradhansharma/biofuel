=====================================
Django Guide App - Developer's Guide
=====================================

This is the developer's guide for the Django Guide App, an application designed to manage and display guides in a Django project. This guide will walk you through the key components of the app, starting with the `admin.py` file.

Admin Configuration (`admin.py`)
----------------------------------

The `admin.py` file is where we define the admin interface for managing our guide-related models. Here, we'll provide an overview of each admin class and its functionality.

1. `GenarelGuideAdmin`:
   - This admin class is used to manage instances of the `GenarelGuide` model.
   - It extends `SummernoteModelAdmin` to enable a rich text editor for the `content` field.
   - The `list_filter` attribute adds a filter for the `menu` field in the admin interface.

```python
@admin.register(GenarelGuide)
class GenarelGuideAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # Enable Summernote for the 'content' field
    list_filter = ('menu',)  # Add a filter for the 'menu' field
```

2. `GuideTypeAdmin`:
   - This admin class is used to manage instances of the `GuideType` model.
   - It includes the `prepopulated_fields` attribute, which automatically generates the `key` field based on the `title` field.
   - If you want the `key` field to be read-only, uncomment the `readonly_fields` attribute.

```python
@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'key': ('title',)}  # Auto-generate 'key' based on 'title'
    # readonly_fields = ('key',)  # Uncomment this line if 'key' should be read-only
```

3. `GuideMenuAdmin`:
   - This admin class is used to manage instances of the `GuideMenu` model.
   - Similar to `GuideTypeAdmin`, it includes the `prepopulated_fields` attribute, which generates the `slug` field based on the `title` field.
   - The `list_filter` attribute adds a filter for the `guidetype` field in the admin interface.

```python
@admin.register(GuideMenu)
class GuideMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate 'slug' based on 'title'
    list_filter = ('guidetype',)  # Add a filter for the 'guidetype' field
```

Installation and Usage
----------------------

To use the Django Guide App in your project, follow these steps:

1. Install the app by adding it to your project's `INSTALLED_APPS` in the project's settings:

   ```python
   INSTALLED_APPS = [
       # ...
       'guide',  # Add 'guide' to your installed apps
       # ...
   ]
   ```

2. Configure the app's database models by running migrations:

   ```bash
   python manage.py makemigrations guide
   python manage.py migrate
   ```

3. Create a superuser to access the admin interface:

   ```bash
   python manage.py createsuperuser
   ```

4. Register your guide-related models in the `admin.py` file as shown above.

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the admin interface at `http://localhost:8000/admin/` and use the registered admin classes to manage guides, guide types, and guide menus.



===============================
Django Guide App - Models Guide
===============================

This is the models guide for the Django Guide App, explaining the structure and attributes of the models defined in the `models.py` file.

Models Overview (`models.py`)
-------------------------------

The `models.py` file defines three main models used in the Django Guide App: `GuideType`, `GuideMenu`, and `GenarelGuide`. Each model represents a different aspect of managing guides.

1. `GuideType` Model:
   - Model representing different types of guides.
   - Attributes:
     - `title` (CharField): The title of the guide type.
     - `position` (IntegerField): The position of the guide type.
     - `key` (SlugField): A slug field used for identifying the guide type.
     - `icon_image` (ImageField): An image field for the guide type's icon.
   - The `__str__` method returns the title of the guide type.
   - The `get_absolute_url` method returns the absolute URL for the guide type.

2. `GuideMenu` Model:
   - Model representing menus for guides.
   - Attributes:
     - `title` (CharField): The title of the guide menu.
     - `position` (IntegerField): The position of the guide menu.
     - `guidetype` (ForeignKey): A foreign key to the associated guide type.
     - `slug` (SlugField): A slug field used for identifying the menu.
   - The `__str__` method returns the title of the guide menu.
   - The `get_absolute_url` method returns the absolute URL for a general guide within this menu.

3. `GenarelGuide` Model:
   - Model representing general guides.
   - Attributes:
     - `title` (CharField): The title of the general guide.
     - `position` (IntegerField): The position of the general guide.
     - `menu` (ForeignKey): A foreign key to the related guide menu.
     - `anchor` (CharField): An anchor field.
     - `parent` (ForeignKey): A foreign key to a parent guide (self-referential relationship).
     - `content` (TextField): The content of the general guide.
   - The `__str__` method returns the title of the general guide along with its parent information.

Usage and Relationships
-----------------------

These models are designed to create a structured system for managing and displaying guides within your Django project. `GuideType` defines the types of guides, `GuideMenu` organizes guides into menus, and `GenarelGuide` contains the actual guide content.

- `GuideType` and `GuideMenu` are related through a foreign key, allowing you to group menus by guide type.
- `GenarelGuide` is related to `GuideMenu` to associate guides with specific menus.

You can further customize these models or add additional fields to suit the specific requirements of your project.

For more information on using Django models, refer to the official Django documentation: https://docs.djangoproject.com/



=============================
Django Guide App - URLs Guide
=============================

This is the URLs guide for the Django Guide App, explaining the URL patterns and their associated views defined in the `urls.py` file.

URL Patterns Overview (`urls.py`)
-----------------------------------

The `urls.py` file defines the URL patterns that map URLs to views within the Django Guide App. Here's an overview of the defined URL patterns:

1. Guide Home Page:
   - URL Pattern: `/guide`
   - View: `views.guide_home`
   - Name: `'guide:guide_home'`
   - Description: This URL pattern maps to the `guide_home` view, which serves as the home page for the guide app.

2. Specific Guide Type:
   - URL Pattern: `/guide/<str:key>`
   - View: `views.guide_type`
   - Name: `'guide:guide_type'`
   - Description: This URL pattern is used to display guides of a specific type. The `key` parameter is a dynamic part of the URL.

3. General Guide Under a Specific Guide Type:
   - URL Pattern: `/guide/<str:gt>/<str:slug>`
   - View: `views.genarel_guide`
   - Name: `'guide:genarel_guide'`
   - Description: This URL pattern is used to display a general guide under a specific guide type. It takes two dynamic parameters, `gt` and `slug`.

Using these URL patterns, you can navigate to different sections of the guide app, view guides of specific types, and access individual general guides.

Namespace and `app_name`
-------------------------

The `'guide'` namespace is set using the `app_name` variable at the beginning of the `urls.py` file. This namespace is used to organize and avoid naming conflicts with URL patterns from other apps in your Django project.

Each URL pattern is associated with a unique name, which can be used for reverse URL lookups or in templates. The names are prefixed with `'guide:'` to specify the namespace.

For example:
- `'guide:guide_home'` refers to the URL pattern for the guide home page.
- `'guide:guide_type'` refers to the URL pattern for displaying guides of a specific type.
- `'guide:genarel_guide'` refers to the URL pattern for displaying a general guide under a specific guide type.



=============================
Django Guide App - Views Guide
=============================

This is the views guide for the Django Guide App, explaining the purpose and functionality of each view defined in the `views.py` file.

Views Overview (`views.py`)
----------------------------

The `views.py` file contains view functions that handle HTTP requests and define the behavior of different pages in the Django Guide App. Here's an overview of each view:

1. `guide_home` View:
   - URL: `/guide`
   - Description: This view function serves as the home page for the guide app. It retrieves information about guide types and renders the home page template with guide type information.
   - Args:
     - `request` (HttpRequest): The request object.
   - Returns:
     - `HttpResponse`: The rendered home page.

2. `guide_type` View:
   - URL: `/guide/<str:key>`
   - Description: This view function displays guides of a specific type. It retrieves guide menus for the specified guide type and renders the guide type template.
   - Args:
     - `request` (HttpRequest): The request object.
     - `key` (str): The key of the guide type.
   - Returns:
     - `HttpResponse`: The rendered guide type page.

3. `genarel_guide` View:
   - URL: `/guide/<str:gt>/<str:slug>`
   - Description: This view function displays a general guide under a specific guide type and menu. It retrieves general guides for the specified guide type and menu and renders the general guide template.
   - Args:
     - `request` (HttpRequest): The request object.
     - `gt` (str): The key of the guide type.
     - `slug` (str): The slug of the guide menu.
   - Returns:
     - `HttpResponse`: The rendered general guide page.

Each view function takes a `request` parameter, which represents the incoming HTTP request, and returns an `HttpResponse` object that represents the rendered HTML page.

Meta Information and SEO
------------------------

Each view includes meta information for SEO (Search Engine Optimization) and social sharing. This information helps improve the visibility and sharing of the guide content. It includes metadata such as titles, descriptions, tags, and images.





Customization
-------------

You can customize the app further to meet your project's specific requirements. For example, you can extend the models, add additional fields, or modify the admin classes to tailor the admin interface to your needs.

For more information on Django development and customization, refer to the official Django documentation: https://docs.djangoproject.com/

Feedback and Contributions
--------------------------

We welcome feedback, bug reports, and contributions to this project. If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository of this project.


Thank you for using the Django Guide App!
```
