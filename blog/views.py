from pprint import pprint
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count, Q 
from doc.doc_processor import site_info
from django.template.defaultfilters import truncatechars
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import html
import re

import logging
log =  logging.getLogger('log')


def post_list(request, tag_slug=None):
    
    """
    View function to display a list of blog posts.

    This view handles displaying a list of all blog posts, posts filtered by a specific tag,
    and search results based on a query string.

    :param request: The HTTP request object.
    :param tag_slug: Optional tag slug to filter posts by a specific tag.
    """ 
    context = {}  
    
    # Get the search query from the request's GET parameters
    query = request.GET.get("q")   
    
    # Clear the stored search term in the session if no search query
    request.session['q'] = ''
    
    
    tag = None
    if tag_slug:
        # Retrieve the Tag object based on the tag_slug or return a 404 response     
        tag = get_object_or_404(Tag, slug=tag_slug) 
        
        log.info(f'{request.user} looking blog by the tag {tag} ')   
          
        # Get posts tagged with the specified tag 
        posts = BlogPost.published.filter(tags__in=[tag]).order_by('-updated')
    elif query:
         # Store the search query in the session to display it in the search box
        request.session['q'] = query
        
        log.info(f'{request.user} searching blog by the text {query} ')   
        
        # Filter posts based on search query using Q objects to search title, tags, and body        
        posts = BlogPost.published.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query) | Q(body__icontains=query)
        ).order_by('-updated').distinct()
    else:
        log.info(f'{request.user} accessed all blog.')  
        
        # Get all published posts
        posts = BlogPost.published.all().order_by('-updated')   
        
        
        
    # Sort the posts queryset based on the total_view property
    ordered_posts = sorted(posts, key=lambda post: post.total_view, reverse=True)    
    most_viewed = posts.filter(pk__in=[post.pk for post in ordered_posts])   
    
    
    # Paginate the posts
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')   
    try:
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  
        
    context['posts'] = posts  
    context['most_viewed'] = most_viewed        
    context['tag'] = tag      
    

    # Set meta information for the page
    meta_data = site_info()    
    meta_data['title'] = f'PUBLISHED BLOG POSTS '
    meta_data['description'] = f"This blog list provides an up-to-date selection of the latest and greatest posts. Get insights on the most current trends, tips, and advice covering a variety of topics."
    meta_data['tag'] = 'blog, gf-vp'
    meta_data['robots'] = 'index, follow'    
    context['site_info'] = meta_data    
    
    return render(request, 'blog/blogs.html', context)


# def html_to_txt(html_text):
#     txt = html.unescape(html_text)
#     tags = re.findall("<[^>]+>",txt)    
#     for tag in tags:
#         txt=txt.replace(tag,'')
#     return txt


def post_detail(request, post):    
    """
    View function to display a detailed view of a blog post.

    This view handles displaying a detailed view of a specific blog post,
    including related posts and meta information.

    :param request: The HTTP request object.
    :param post: The slug of the specific blog post to display.
    """
    context = {}
    
    
    # Clear the stored search term in the session
    request.session['q'] = ''
    
    # Get the search query from the request's GET parameters   
    query = request.GET.get("q")   
    
    if query:
        log.info(f'{request.user} searching blog by the text {query}, so redirecting to the blog list as per search result')   
        # Store the search query in the session and redirect to the post_list view with the query
        request.session['q'] = query
        return HttpResponseRedirect(reverse('blog:post_list') + '?q=' + query)
        
    log.info(f'Accessed blog {post} by user {request.user} ')  
    
    # Retrieve the specific published blog post based on the slug 
    post = get_object_or_404(BlogPost, slug=post, status='published')
    
    # Record the view action for the blog post
    post.view(request)   
    
    # Retrieve the IDs of tags associated with the post
    post_tags_id = post.tags.values_list('id', flat=True)
    
    # Get similar posts based on shared tags, excluding the current post
    similar_posts = BlogPost.published.filter(tags__in = post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:6] 
    
    context = {
        'post':post,
        'similar_posts':similar_posts        
    }  
    
   
    # Set meta information for the page
    meta_data = site_info()    
    meta_data['title'] = post.title 
    meta_data['description'] = re.sub(r'&nbsp;', '', truncatechars(strip_tags(mark_safe(post.body)), 160))
    meta_data['tag'] = 'blog, gf-vp'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = post.image.url    
    context['site_info'] = meta_data                
    
    return render(request, 'blog/post_detail.html', context = context)

