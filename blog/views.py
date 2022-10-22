

from pprint import pprint
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from blog.forms import CommentForm, BlogForm
from taggit.models import Tag
from django.db.models import Count, Q 
from .forms import *
import logging
log =  logging.getLogger('log')


import requests

def post_list(request, tag_slug=None):
 
    context = {}  
    
    #recrding query if anybody searcing the block using blog search form  
    query = request.GET.get("q")   
    
    #Below will ensure there is no search term in the searc box if no body searching using search box.   
    request.session['q'] = ''
    
    
    tag = None
    if tag_slug:
        #If there is tag slug in the url then output tagged result otherwise 404        
        tag = get_object_or_404(Tag, slug=tag_slug) 
        
        log.info(f'{request.user} looking blog by the tag {tag} ')   
          
        #If tag in posts's tag in the url will return the posts     
        posts = BlogPost.published.filter(tags__in=[tag]).order_by('-updated')
    elif query:
        #Search term recording as session to view in the serarch box while showing result.
        request.session['q'] = query
        
        log.info(f'{request.user} searching blog by the text {query} ')   
        
        #if searching will return the result. Here I am using Q to speedup search. Q will search search term in title, tag and in body. and will return distinct result.
        posts = BlogPost.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query) | Q(body__icontains=query)).order_by('-updated').distinct()
    else:
        log.info(f'{request.user} accessed all blog.')  
        #Otherwise will return all result
        posts = BlogPost.published.all().order_by('-updated')   
    
    #Response will be paginated    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')   
    try:
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  
        
    context['posts'] = posts
    context['pages'] = page    
    context['tag'] = tag      
    return render(request, 'blog/blogs.html', context)

def post_detail(request, post): 
    #Below will ensure there is no search term in the searc box if no body searching using search box. 
    request.session['q'] = ''
    #recrding query if anybody searcing the block using blog search form   
    query = request.GET.get("q")   
    if query:
        log.info(f'{request.user} searching blog by the text {query}, so redirecting to the blog list as per search result')   
        #Search term recording as session to view in the serarch box while showing result.
        request.session['q'] = query
        return HttpResponseRedirect(reverse('blog:post_list') + '?q=' + query)
        
    log.info(f'Accessed blog {post} by user {request.user} ')   
    post = get_object_or_404(BlogPost, slug=post, status='published')
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = BlogPost.published.filter(tags__in = post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:6] 
    
    context = {
        'post':post,
        'similar_posts':similar_posts        
    }             
    
    return render(request, 'blog/post_detail.html', context = context)