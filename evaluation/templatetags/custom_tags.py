from django import template

register = template.Library()


# A custom tag to wrap and line break a=based on argument supplied in template
@register.filter(name='brek_after_two')
def brek_after_two(value, arg):
    first_line =  str(value)[:arg]
    last_line =  str(value)[-arg:]    
    text = f"{first_line} </br> {last_line}"        
    return str(text)



@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter(name='in_quot') 
def in_quot(quote, user): 
    quotes = quote.filter(service_provider=user)
    
    return quotes

@register.filter(name='offchars') 
def offchars(value, arg): 
    return value[arg:]

@register.filter(name='onnchars') 
def onnchars(value, arg):  
    return value[:arg]

@register.filter(name='listobj_for_paginator') 
def listobj_for_paginator(value, request):  
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(value, 5)
    page_number = request.GET.get('page')
    sugestions_obj = paginator.get_page(page_number)
    
    return sugestions_obj