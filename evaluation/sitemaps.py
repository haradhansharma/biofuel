from django.contrib import sitemaps
from django.urls import reverse
from accounts.models import UserType
from blog.models import *
from crm.models import *
from doc.models import *
from .models import *
from glossary.models import *
from guide.models import *
from home.models import *
from django.contrib.auth import get_user_model



class GfvpSitemap(sitemaps.Sitemap):
    """
    Sitemap for the GFVP (Green Fuel Validation Platform) website.

    This sitemap includes various important URLs for the website.

    Attributes:
        priority (float): The priority of this sitemap in relation to others (0.0 to 1.0).
        changefreq (str): The expected change frequency of URLs in this sitemap.

    """
    priority = 0.5
    changefreq = 'monthly'   
    

    def items(self):
        """
        Define the list of URLs to include in the sitemap.

        Returns:
            list: A list of URL names.

        """
        
        # Define URL name constants
        ACCOUNTS_SIGNUP = 'accounts:signup'
        ACCOUNTS_LOGIN = 'accounts:login'
        BLOG_LIST = 'blog:post_list'
        CRM_LEADS = 'crm:leads'
        CRM_SUBSCRIPTION = 'crm:subscription'
        EVALUATION = 'evaluation:evaluation2'
        GDPR = 'gdpr'
        TERM = 'term'
        GROSSARY = 'glossary:g_list'     
        HOME = 'home:home'
        DASHBOARD = 'home:dashboard'
        USER_SETTINGS = 'home:user_settings'
        DASHBOARD = 'home:dashboard'
        QUESTION_INIT = 'home:questionsint'
        DASHBOARD = 'home:dashboard'
        QUOTATION = 'home:quotations'
        
        return [
            ACCOUNTS_SIGNUP, 
            ACCOUNTS_LOGIN, 
            BLOG_LIST, 
            CRM_LEADS,          
            CRM_SUBSCRIPTION,
            EVALUATION, 
            GDPR,
            TERM, 
            GROSSARY,             
            HOME,
            DASHBOARD,
            USER_SETTINGS,
            QUESTION_INIT,
            QUOTATION,             
            
            ] 
        
        
    def location(self, item):
        """
        Generate the URL for a given item using its name.

        Args:
            item (str): The name of the URL.

        Returns:
            str: The full URL for the given item.

        """
        return reverse(item)      
    
class UserSitemap(sitemaps.Sitemap):
    """
    Sitemap for user profiles on the GFVP website.

    This sitemap includes user profiles who are active and have verified email addresses.

    Attributes:
        changefreq (str): The expected change frequency of URLs in this sitemap.
        priority (float): The priority of this sitemap in relation to others (0.0 to 1.0).

    """
    changefreq = "monthly"
    priority = 0.5    

    def items(self):
        """
        Retrieve the list of active users with verified email addresses.

        Returns:
            QuerySet: A queryset containing user profiles.

        """
        Users = get_user_model()
        users = Users.objects.filter(is_active = True, email_verified = True).order_by('-date_joined')
        return users
    
    def lastmod(self, obj):
        """
        Determine the last modification date for a user profile.

        Args:
            obj (User): The user profile.

        Returns:
            datetime: The date the user profile was last modified.

        """
        return obj.date_joined
        
    def location(self, obj):
        """
        Generate the URL for a user's profile.

        Args:
            obj (User): The user profile.

        Returns:
            str: The URL for the user's profile.

        """
        return reverse('accounts:user_link')
    
class UserTypeSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.5    

    def items(self):
        """
        Retrieve the list of active Usertype.

        Returns:
            QuerySet: A queryset containing user type.

        """        
        types = UserType.objects.filter(active = True).order_by('-sort_order')
        return types
    
    def lastmod(self, obj):
        """
        Determine the last modification date for a user type.

        Args:
            obj (UserType): The user type.

        Returns:
            datetime: The date the user type was last modified.

        """
        
        return obj.created
        
    def location(self, obj):    
        """
        Generate the URL for a user types.

        Args:
            obj (UserType): The user type.

        Returns:
            str: The URL for the user type page.

        """    
        return reverse('types', args=[str(obj.slug)])
    
class BlogSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        """
        Retrieve the list of published Blogpost.

        Returns:
            QuerySet: A queryset containing blog post.

        """
        return BlogPost.published.all().order_by('-updated')  
    
    def lastmod(self, obj):
        """
        Determine the last modification date for a blogpost.

        Args:
            obj (BlogPost): The blogpost.

        Returns:
            datetime: The date the blogpost was last modified.

        """
        return obj.updated
        
    def location(self, obj):
        """
        Generate the URL for a blog post.

        Args:
            obj (BlogPost): The Blog.

        Returns:
            str: The URL for the blog post.

        """
        return reverse('blog:post_detail', args=[str(obj.slug)])
    
class HtmlReportitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        """
        Retrieve the list of genarated evaluation report with verified email addresses.

        Returns:
            QuerySet: A queryset containing evaluation report.

        """
        return Evaluator.objects.filter(report_genarated = True).order_by('-update_date')  
    
    def lastmod(self, obj):
        """
        Determine the last modification date for a evaluation report.

        Args:
            obj (Evaluator): The a evaluation report.

        Returns:
            datetime: The date the a evaluation report was last modified.

        """
        return obj.update_date
        
    def location(self, obj):
        """
        Generate the URL for a evaluation's report.

        Args:
            obj (Evaluator(report)): The evaluation report.

        Returns:
            str: The URL for the evaluation's report.

        """
        return reverse('evaluation:nreport', args=[str(obj.slug)])
    
    

    
 
      
               
    