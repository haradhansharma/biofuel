---
title: Technical Guide Doc app of GFVP
summary: Here given overview of the Doc app of Green fuel validation platform.
copyright: (c) gf-vp.com
repo_url: https://github.com/haradhansharma/biofuel
edit_uri: blob/v24123/gfvp_docs/docs
authors:
    - Haradhan Sharma
date: 2023-10-16

---

# GFVP Doc APP


## Introduction


The 'doc' app is a Django application designed to manage and organize common functions and behaviors. This README provides an overview of the app and explains the structure and functionality of the `admin.py` file.

## `admin.py` Overview


The `admin.py` file within the 'doc' app is essential for customizing the admin interface of the Django application. It extends the default admin behavior for models and provides a more tailored experience for managing content.

Below is an explanation of the key components in `admin.py`:

1. **Model Registration**:

   - We register the 'Acordion' model with the admin site using `admin.site.register(Acordion)`. This enables administrators to manage 'Acordion' objects through the Django admin panel.

2. **Inline Admin Class**:

   - We define an inline admin class, `ExtendSiteOfSite`, which inherits from `admin.StackedInline`. This class allows for the management of 'ExSite' objects within the 'Site' admin page. The `can_delete` attribute is set to `False`, preventing the deletion of 'ExSite' instances from the 'Site' admin interface.

3. **Customized 'Site' Admin**:

   - The `SiteAdmin` class customizes the admin interface for the 'Site' model. It specifies the fields to be displayed in the list view using `list_display` and enables search functionality by defining the fields in `search_fields`. Additionally, it includes the `ExtendSiteOfSite` inline admin class, providing a comprehensive view of 'Site' and its related 'ExSite' instances.

4. **Unregister and Re-register**:

   - To apply the customizations, we unregister the default 'Site' admin using `admin.site.unregister(Site)` and then re-register it with our custom `SiteAdmin` class using `admin.site.register(Site, SiteAdmin)`.

With these configurations in `admin.py`, administrators can efficiently manage 'Acordion', 'Site', and their related 'ExSite' objects, ensuring a smooth user experience while interacting with document-related content within the Django admin panel.

Please refer to the respective model files and other parts of the application for more detailed information on their functionalities and relationships.

## Getting Started


To get started with the 'doc' app, follow these steps:

1. Install the app in your Django project.

2. Configure the app's models, views, and templates as needed for your specific document management requirements.

3. Customize the 'admin.py' file to suit your admin interface preferences, as demonstrated in this README.

4. Run migrations to apply database changes: `python manage.py makemigrations` and `python manage.py migrate`.

5. Create superuser accounts to access the admin panel: `python manage.py createsuperuser`.

6. Start the development server: `python manage.py runserver`.

7. Access the Django admin panel, where you can manage 'Acordion', 'Site', and 'ExSite' objects with the customizations provided in `admin.py`.



## 'doc_processor.py' 


### Introduction

The 'doc_processor.py' module in the 'doc' app is a crucial component responsible for processing common data and site information used throughout the application. This README provides an overview of the functions and their purposes within this module.

### Functions Overview

1. **site_info()**:

   - This function retrieves and caches site information such as name, domain, meta information, logos, contact details, and more.
   - It enhances performance by caching the retrieved information.
   - Usage:
       ```python
       site_information = site_info()
       ```

2. **get_pending_suggestion()**:

   - Retrieves and caches the count of pending suggestions from the 'Suggestions' model.
   - This function is used to optimize performance by caching the count for future use.
   - Usage:
       ```python
       pending_suggestion_count = get_pending_suggestion()
       ```

3. **common_doc(request)**:

   - Generates common data required for rendering templates, including text translations, site information, menus, and subscription forms.
   - Accepts an `HttpRequest` object as input to cater to request-specific data.
   - Usage:
       ```python
       common_data = common_doc(request)
       ```

### Usage Instructions

To utilize the 'doc_processor.py' module in your 'doc' app, follow these steps:

1. Import the necessary functions into your views or other modules where common data is required.

2. Use the functions as outlined in their respective descriptions above.

For example, to access site information and common data:

```python
from doc_processor import site_info, common_doc

# Access site information
site_information = site_info()

# Access common data for rendering templates
common_data = common_doc(request)
```


## 'models.py' in the 'doc' App


### Introduction

The `models.py` module within the 'doc' app defines the database models used to store and manage data related to site information and accordion elements. This README provides an overview of the models and their attributes.

### Models Overview

1. **ExSite**:

    - Represents extended site information associated with a Django Site.
    - Stores metadata, logos, contact details, and social media links for the site.
    - Attributes:
        - `site` (OneToOneField): Relationship with the Django Site model.
        - `site_meta` (CharField): Meta information for the site.
        - `site_description` (TextField): A longer description for the site.
        - `site_meta_tag` (CharField): Meta tag for the site.
        - `site_favicon` (ImageField): Site favicon image.
        - `site_logo` (ImageField): Site logo image.
        - `slogan` (CharField): A short slogan or tagline for the site.
        - `og_image` (ImageField): Open Graph image for social sharing.
        - `mask_icon` (FileField): SVG file for mask icon.
        - `phone` (CharField): Contact phone number.
        - `email` (EmailField): Contact email address.
        - `location` (CharField): Physical location or address.
        - `facebook_link` (URLField): Facebook profile URL.
        - `twitter_link` (URLField): Twitter profile URL.
        - `linkedin_link` (URLField): LinkedIn profile URL.
        - `qualified_ans_range` (IntegerField): A numeric value representing a qualification range.
    - Managers:
        - `objects` (models.Manager): The default manager.
        - `on_site` (CurrentSiteManager): Manager for filtering by the current site.

2. **Acordion**:

    - Represents an accordion element with a button and description.
    - Contains a button with text and a description and allows associating the accordion with an installed app.
    - Attributes:
        - `button_text` (CharField): Text displayed on the button.
        - `button_des` (TextField): Description or content associated with the accordion element.
        - `apps` (CharField): Choice field for associating the accordion with an installed app.

### Usage Instructions


To utilize the models defined in `models.py` within your 'doc' app, follow these steps:

1. Create migrations and apply them to your database using the `makemigrations` and `migrate` management commands.

2. Use the models in your application's views, forms, or other modules as needed. For example, you can create, retrieve, update, or delete instances of `ExSite` or `Acordion` in your views.

3. Customize the models and their attributes as per your project's requirements. You can add new fields or methods to extend their functionality.

For detailed information on working with Django models, please refer to the official Django documentation.


For further information and detailed documentation, consult the project's documentation or the source code.

## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.



## Credits

This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).
