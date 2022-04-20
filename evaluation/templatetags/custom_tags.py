from django import template

register = template.Library()


# A custom tag to wrap and line break a=based on argument supplied in template
@register.filter(name='brek_after_two')
def brek_after_two(value, arg):
    first_line =  str(value)[:arg]
    last_line =  str(value)[-arg:]    
    text = f"{first_line} </br> {last_line}"        
    return str(text)