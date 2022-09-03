

from pprint import pprint
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from blog.forms import CommentForm, BlogForm
from taggit.models import Tag
from django.db.models import Count, Q 
from .forms import *


import requests

def post_list(request, tag_slug=None):
 
    context = {}    
    posts = BlogPost.published.all()#using custom manager    
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts=posts.filter(tags__in=[tag])    
            
    query = request.GET.get("q")      
    if query:
        posts=BlogPost.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
    
    
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
       
    post = get_object_or_404(BlogPost, slug=post, status='published')
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = BlogPost.published.filter(tags__in = post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:6] 
    
    context = {
        'post':post,
        'similar_posts':similar_posts        
    }             
    
    return render(request, 'blog/post_detail.html', context = context)