from django import template

register = template.Library()

# A custom tag to wrap and line break a=based on argument supplied in template
@register.filter(name='brek_after_two')
def brek_after_two(value, arg):
    """
    Custom template filter to wrap text and insert a line break after a specified number of characters.

    Args:
        value (str): The input text.
        arg (int): The number of characters after which to insert the line break.

    Returns:
        str: The input text with a line break inserted after the specified number of characters.
    """
    first_line =  str(value)[:arg]
    last_line =  str(value)[-arg:]    
    text = f"{first_line} </br> {last_line}"        
    return str(text)

@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Custom template tag to get the verbose name of a field in a model.

    Args:
        instance (Model): The model instance.
        field_name (str): The name of the field.

    Returns:
        str: The verbose name of the field in title case.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter(name='in_quot') 
def in_quot(quote, user): 
    """
    Custom template filter to filter quotes based on a specific user.

    Args:
        quote (QuerySet): The queryset of quotes.
        user (User): The user for whom quotes should be filtered.

    Returns:
        QuerySet: The filtered queryset of quotes for the specified user.
    """
    quotes = quote.filter(service_provider=user)    
    return quotes

@register.filter(name='offchars') 
def offchars(value, arg): 
    """
    Custom template filter to return characters from the end of a string.

    Args:
        value (str): The input string.
        arg (int): The number of characters to return from the end.

    Returns:
        str: The specified number of characters from the end of the input string.
    """
    return value[arg:]

@register.filter(name='onnchars') 
def onnchars(value, arg):  
    """
    Custom template filter to return characters from the beginning of a string.

    Args:
        value (str): The input string.
        arg (int): The number of characters to return from the beginning.

    Returns:
        str: The specified number of characters from the beginning of the input string.
    """
    return value[:arg]

@register.filter(name='listobj_for_paginator') 
def listobj_for_paginator(value, request):  
    """
    Custom template filter to paginate a list of objects.

    Args:
        value (list): The list of objects to paginate.
        request (HttpRequest): The HTTP request object.

    Returns:
        Page: The paginated Page object.
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(value, 5)
    page_number = request.GET.get('page')
    sugestions_obj = paginator.get_page(page_number)
    
    return sugestions_obj


@register.filter(name='get_options') 
def get_options(question): 
    """
    Custom template filter to get options associated with a question.

    Args:
        question (Question): The question for which options are retrieved.

    Returns:
        list: A list of options associated with the question.
    """
    from evaluation.helper import get_options_of_ques
    options = get_options_of_ques(question) 
    return options


@register.filter(name='get_quotations_user') 
def get_quotations_user(ques, user): 
    """
    Custom template filter to get quotations related to a question for a specific user.

    Args:
        ques (Question): The question for which quotations are retrieved.
        user (User): The user for whom quotations should be retrieved.

    Returns:
        list: A list of quotations associated with the question and user.
    """
    quotations = [quotation for quotation in ques.get_quotations if user == quotation.service_provider]
    if quotations:
        return quotations
    return []


@register.filter(name='get_related_quotations_user') 
def get_related_quotations_user(ques, user): 
    """
    Custom template filter to get related quotations for a question for a specific user.

    Args:
        ques (Question): The question for which related quotations are retrieved.
        user (User): The user for whom related quotations should be retrieved.

    Returns:
        list: A list of related quotations associated with the question and user.
    """
    quotations = [quotation for quotation in ques.get_related_quotations if user == quotation.service_provider]
    if quotations:
        return quotations
    return []

@register.filter(name='get_merged_quotations_with_user') 
def get_merged_quotations_with_user(ques, user):
    """
    Custom template filter to get merged quotations for a question with a specific user.

    Args:
        ques (Question): The question for which merged quotations are retrieved.
        user (User): The user for whom merged quotations should be retrieved.

    Returns:
        list: A list of merged quotations associated with the question and user.
    """
    quotations = [quotation for quotation in ques.get_merged_quotations if quotation.service_provider == user]
    if quotations:
        return quotations
    return []

@register.filter(name='get_types_slug') 
def get_types_slug(type):
    """
    Custom template filter to retrieve the slug of a UserType based on its type.

    Args:
        type (str): The type of UserType ('is_producer', 'is_expert', 'is_consumer', 'is_marine').

    Returns:
        str or None: The slug of the UserType associated with the provided type, or None if not found.

    Note:
        This custom template filter helps retrieve the slug of a UserType based on the provided type.
        It checks the type and returns the corresponding slug, or None if the type is not recognized.
    """
    from accounts.models import UserType
    
    # Check the provided type and retrieve the corresponding UserType's slug.
    if type == 'is_producer':
        slug = UserType.objects.filter(is_producer = True).first().slug
    elif type == 'is_expert':
        slug = UserType.objects.filter(is_expert = True).first().slug
    elif type == 'is_consumer':
        slug = UserType.objects.filter(is_consumer = True).first().slug
    elif type == 'is_marine':
        slug = UserType.objects.filter(is_marine = True).first().slug  
    else:
        slug = None

    return slug


