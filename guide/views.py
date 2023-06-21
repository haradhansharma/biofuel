from django.shortcuts import render
from .models import * 
from doc.doc_processor import site_info
from django.templatetags.static import static


def guide_home(request):     
    guide_type = GuideType.objects.all().order_by('position')  
    
    context = {
        "guide_type": guide_type,          
    }
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'User guide Home' 
    meta_data['description'] = 'This is the landing page for user guide build for Green fuel validation platform'
    meta_data['tag'] = 'guide, gf-vp'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = 'guide/logo-02.png'
    
    context['site_info'] = meta_data    
    return render(request, 'guide/bg_home.html', context = context)

def guide_type(request, key):    
    guide_general_menu = GuideMenu.objects.filter(guidetype = GuideType.objects.get(key=key)).order_by('position')      
    guidetype = GuideType.objects.filter(key=key).order_by('position')   
    
    context = {
        "guidetype": guidetype,
        'guide_general_menu' : guide_general_menu
    }
    #meta
    meta_data = site_info()    
    meta_data['title'] = guidetype.get(key=key).title
    meta_data['description'] = 'This is the landing page for user guide build for Green fuel validation platform'
    meta_data['tag'] = 'guide type, gf-vp'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = guidetype.get(key=key).icon_image.url
    
    context['site_info'] = meta_data  
    return render(request, 'guide/bg_guide_type.html', context = context)


    
def genarel_guide(request, gt, slug):
    guide_type = GuideType.objects.get(key=gt)
    guide_general_menu = GuideMenu.objects.filter(guidetype =  guide_type).order_by('position')      
    guide = GenarelGuide.objects.filter(menu = guide_general_menu.get(slug=slug)).order_by('position')       
    
    context = {
        'guide_general_menu' : guide_general_menu ,
        'guide' : guide ,      
    }
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = guide[0].title if guide.exists() else slug
    meta_data['description'] = 'Details instruction'
    meta_data['tag'] = 'guide type, gf-vp'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = guide_type.icon_image.url
    
    context['site_info'] = meta_data  
    return render(request, 'guide/bg_genarel_guide.html', context = context)
        