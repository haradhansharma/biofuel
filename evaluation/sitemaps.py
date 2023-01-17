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
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'accounts:signup', 
            'accounts:login', 
            'blog:post_list', 
            'crm:leads', 
            'crm:leads',
            'crm:subscription',
            'evaluation:evaluation2', 
            'gdpr',
            'term', 
            'glossary:g_list', 
            'guide:guide_home',
            'home:home',
            'home:dashboard',
            'home:user_settings',
            'home:questions',
            'home:quotations',
             
            
            ] 
        
        
    def location(self, item):
        return reverse(item)      
    
class UserSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        Users = get_user_model()
        users = Users.objects.filter(is_active = True, email_verified = True).order_by('-date_joined')
        return users
    
    def lastmod(self, obj):
        return obj.date_joined
        
    def location(self, obj):
        # return "/accounts/%s"  % (obj.username)
        return reverse('accounts:user_link', args=[str(obj.username)])
    
class UserTypeSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.5    

    def items(self):
        
        types = UserType.objects.filter(active = True).order_by('-sort_order')
        return types
    
    # def lastmod(self, obj):
    #     return obj.sort_order
        
    def location(self, obj):
        # return "/types/%s"  % (obj.slug)
        return reverse('types', args=[str(obj.slug)])
    
class BlogSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return BlogPost.published.all().order_by('-updated')  
    
    def lastmod(self, obj):
        return obj.updated
        
    def location(self, obj):
        return reverse('blog:post_detail', args=[str(obj.slug)])
    
class HtmlReportitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return Evaluator.objects.filter(report_genarated = True).order_by('-update_date')  
    
    def lastmod(self, obj):
        return obj.update_date
        
    def location(self, obj):
        return reverse('evaluation:nreport', args=[str(obj.slug)])
    
    

    
 
      
               
    