from pprint import pprint
from django.shortcuts import render
from .models import *

# Create your views here.
def guide_home(request):
    
    

     
    guide_type = GuideType.objects.all()
    context = {
        "guide_type": guide_type,    
        
    }
    return render(request, 'guide/home.html', context = context)

def guide_type(request, key):

    
    guide_general_menu = GuideMenu.objects.filter(type = GuideType.objects.get(key=key))    
    type = GuideType.objects.filter(key=key)  
    
    context = {
        "type": type,
        'guide_general_menu' : guide_general_menu
    }
    return render(request, 'guide/guide_type.html', context = context)


    
def genarel_guide(request, slug, type):
    guide_general_menu = GuideMenu.objects.filter(type =  GuideType.objects.get(key=type))  
    
    guide = GenarelGuide.objects.filter(menu = guide_general_menu.get(slug=slug))
      
    
    context = {
        'guide_general_menu' : guide_general_menu ,
        'guide' : guide     ,
        
        'aaa' : 'asdasdasdasdasdasd'
    }
    return render(request, 'guide/genarel_guide.html', context = context)
        