GFVP Blog App
================

Introduction
------------

The GFVP Blog App is a simple yet powerful application that provides the foundation for creating and managing blog posts. This app allows you to easily create, edit, publish, and manage blog posts, while also providing a user-friendly interface for the admin panel.

Installation
------------

To use the Django Blog App in your project, follow these steps:

1. Install the app using pip:

    .. code-block:: bash

       pip install ....

2. Add `'blog'` to the `INSTALLED_APPS` list in your project's `settings.py`:

    .. code-block:: python

       INSTALLED_APPS = [
           # ...
           'blog',
           # ...
       ]

3. Include the app's URLs in your project's `urls.py`:

    .. code-block:: python

       from django.urls import path, include

       urlpatterns = [
           # ...
           path('blog/', include('blog.urls')),
           # ...
       ]

Usage
-----

**Admin Panel:**

The Django Blog App provides an admin panel interface to manage blog posts easily. You can access the admin panel at `/admin/`.

In the admin panel, you can:

- Create, edit, and delete blog posts.
- Use the Summernote rich text editor to compose blog post content.
- Manage tags and categories associated with blog posts.
- Publish or draft blog posts.
- Filter and search for blog posts.

**Customization:**

The app is designed to be easily customizable to fit your project's specific needs. You can extend the `BlogPost` model or modify its behavior by creating your own customizations.

For more information on how to customize and extend the app, refer to the official documentation.


Models
------

The Django Blog App includes two main models to manage blog posts and track actions on various objects.

**Action Model:**

The `Action` model tracks different actions performed on various objects. It's a generic model that can be used to record actions like views and likes on different content types. The key attributes of this model are:

- `content_type`: A ForeignKey to the ContentType model, representing the type of the content object.
- `object_id`: A PositiveIntegerField representing the ID of the content object.
- `content_object`: A GenericForeignKey that allows you to link to any object using the `content_type` and `object_id`.
- `user`: A ForeignKey to the user who performed the action (if authenticated), or `None` for anonymous users.
- `ip_address`: A GenericIPAddressField to store the IP address of the user performing the action.
- `action_type`: A CharField to store the type of action, such as 'view' or 'like'.
- `timestamp`: A DateTimeField representing the time the action was recorded.

This model is designed to be versatile and can be easily extended to track other types of actions as well.

**BlogPost Model:**

The `BlogPost` model represents a blog post within the application. It includes fields to store information about the post's title, content, author, publishing status, and more. The main attributes of this model are:

- `title`: A CharField representing the title of the blog post.
- `image`: An ImageField to store the featured image of the post.
- `slug`: A SlugField to generate and store a URL-friendly slug for the post's URL.
- `author`: A ForeignKey to the user who authored the post.
- `body`: A TextField to store the content of the blog post.
- `publish`: A DateTimeField indicating the publication date and time of the post.
- `created`: A DateTimeField representing the creation date of the post.
- `updated`: A DateTimeField indicating the last update time of the post.
- `status`: A CharField indicating the publishing status of the post (draft or published).
- `tags`: A TaggableManager that allows you to associate tags with the post.
- `actions`: A GenericRelation to the `Action` model, enabling tracking of actions related to this post.

Additionally, the `BlogPost` model includes custom methods to calculate the total number of views and record new views. The model also features a custom manager, `PublishedManager`, to retrieve only published posts.

This combination of models provides a powerful foundation for creating and managing blog posts with customizable features and actions tracking.


Signals
-------

The Django Blog App uses signals to automate certain actions and tasks related to blog posts. Signals allow the app to respond to events like creating, updating, or deleting a blog post, and perform additional actions as needed.

**send_to_mail_queue Signal:**

The `send_to_mail_queue` signal handler is triggered after a `BlogPost` instance is saved. This signal is responsible for creating or updating `BlogMailQueue` entries based on the status and changes to the blog post. The key functionality includes:

- When a new `BlogPost` is created and its status is 'published', a `BlogMailQueue` entry will be created for each subscribed lead.
- If a `BlogPost` is updated and its status is changed to 'draft', any unprocessed `BlogMailQueue` entries related to that post will be deleted.
- If the status of an updated `BlogPost` is changed to 'published' and there are no existing `BlogMailQueue` entries, new entries will be created for each subscribed lead.

**delete_mail_queues Signal:**

The `delete_mail_queues` signal handler is triggered after a `BlogPost` instance is deleted. This signal is responsible for deleting any unprocessed `BlogMailQueue` entries related to the deleted blog post.

To ensure these signals work correctly, the following components must be present:

- Import the necessary models at the beginning of the `signal.py` file.
- Set up appropriate logging to track the actions of the signals.

Please note that signals can greatly enhance the automation and logic within your app, but it's important to use them judiciously and ensure they're thoroughly tested to avoid unintended consequences.

For more information on how signals work in Django and how to handle them effectively, refer to the official Django documentation on signals.


URL Patterns
------------

The Django Blog App uses URL patterns to define how different URLs should be handled and routed to specific views. URL patterns play a crucial role in determining how users can access various parts of your application.

**URL Configuration:**

In the `urls.py` file of the `blog` app, you will find a list of URL patterns defined using the `path` function. Each pattern consists of a URL route and a corresponding view function. The `app_name` is set to 'blog' to create a namespace for these URL patterns.

**URL Patterns Explained:**

1. `blog/`:
   - URL Route: `blog/`
   - View Function: `views.post_list`
   - Name: `post_list`
   - Description: This URL pattern maps to the `post_list` view, which displays a list of all blog posts.

2. `blog/<slug:post>/`:
   - URL Route: `blog/<slug:post>/`
   - View Function: `views.post_detail`
   - Name: `post_detail`
   - Description: This URL pattern includes a slug parameter, which is used to identify a specific blog post. It maps to the `post_detail` view, showing the detailed view of the selected blog post.

3. `blog/tag/<slug:tag_slug>/`:
   - URL Route: `blog/tag/<slug:tag_slug>/`
   - View Function: `views.post_list`
   - Name: `post_tag`
   - Description: This URL pattern includes a slug parameter (`tag_slug`), allowing users to view blog posts filtered by a specific tag. It maps to the `post_list` view, displaying posts associated with the selected tag.

**Namespace and Reversing:**

The `app_name` is set to 'blog', creating a namespace for these URL patterns. This namespace helps avoid naming conflicts and makes it easier to reverse URLs in templates and code using the `app_name:pattern_name` syntax.

For example, to generate the URL for the `post_detail` view for a blog post with the slug 'my-blog-post', you can use `{% url 'blog:post_detail' post='my-blog-post' %}` in templates or `reverse('blog:post_detail', args=['my-blog-post'])` in Python code.

Understanding and utilizing these URL patterns is crucial for ensuring smooth navigation and interaction within the Django Blog App.

For more information on Django URL routing and reversing, refer to the official Django documentation on URL dispatch and URL reversing.


View: post_list
================

The `post_list` view function is responsible for displaying a list of blog posts on the website. This view supports various scenarios, such as showing all published posts, filtering posts by a specific tag, and providing search functionality.

View Details
-------------

**Function Signature:**

   .. code-block:: python

      def post_list(request, tag_slug=None):

**Parameters:**

- `request` (:class:`~django.http.request.HttpRequest`): The HTTP request object.
- `tag_slug` (:class:`~str`, optional): An optional tag slug to filter posts by a specific tag.

**Functionality:**

- This view handles the display of blog posts and supports filtering by tag and searching by query.
- It constructs a context for rendering the template, including the list of blog posts and other necessary data.
- If a `tag_slug` is provided in the URL, it filters posts tagged with the specified tag.
- If a search query (`q`) is present in the GET parameters, it filters posts based on the search query using Q objects for more advanced searches.
- The resulting list of posts is ordered by their update date and supports pagination.

**Stored Search Query:**

If a search query is provided, the view stores it in the user's session to pre-fill the search box when displaying the search results. The stored query is cleared from the session if there is no active search.

**Meta Information:**

The view also sets up meta information for the page, such as title, description, tags, and robot indexing instructions.

Usage Examples
--------------

- To display all published blog posts, access the URL: ``/blog/``
- To view posts with a specific tag, access the URL: ``/blog/tag/tag-slug/``
- To search for specific terms within blog posts, add a search query to the URL: ``/blog/?q=search-term``

This view plays a central role in providing users with a curated list of blog posts and facilitates easy navigation and discovery.

For more information on how this view is utilized within the application and its interaction with templates, please refer to the comments and docstrings within the source code.


View: post_detail
==================

The `post_detail` view function is responsible for displaying a detailed view of a specific blog post on the website. This view provides users with comprehensive information about a single blog post, including related posts and meta information.

View Details
-------------

**Function Signature:**

  .. code-block:: python

     def post_detail(request, post):

**Parameters:**

- `request` (:class:`~django.http.request.HttpRequest`): The HTTP request object.
- `post` (:class:`~str`): The slug of the specific blog post to display.

**Functionality:**

- This view handles the detailed display of a specific blog post.
- It clears any stored search term in the session to ensure a clean user experience.
- If a search query (`q`) is present in the GET parameters, it stores the query in the session and redirects to the `post_list` view to display search results.
- The view retrieves the specific published blog post based on the provided slug.
- It records the view action for the blog post using the `post.view()` method.
- The view fetches similar posts based on shared tags, excluding the current post. These similar posts are ordered by tag similarity and publishing date.
- The view constructs a context for rendering the template, including the detailed blog post and related/similar posts.

**Meta Information:**

The view sets up meta information for the page, including title, description, tags, and robot indexing instructions. It also sets an Open Graph (og) image for social media sharing.

Usage Examples
--------------

- To view the details of a specific blog post, access the URL: ``/blog/my-blog-post/``

The `post_detail` view provides users with a rich and engaging experience to explore the content of individual blog posts and discover related content.

For more insights into how this view interacts with templates and how its features are utilized within the application, refer to the comments and docstrings within the source code.


Contributing
------------

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the project's GitHub repository: https://github.com/yourusername/django-blog-app

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

Credits
-------

This app was developed with love by the Django community.

Contact
-------

If you have any questions or need assistance, you can reach out to us at haradhan.sharma@gmail.com.
