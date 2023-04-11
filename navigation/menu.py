from django.urls import reverse

def dashboard_menu(request):
    
    menu_items = []
    
    menu_items.append(
        {'title': 'Dashboard', 'url': reverse('home:dashboard'), 'data_set': False, 'childs': False, 'icon': '<i class="fa-solid fa-chart-line"></i>'},                            
        )  
    if (request.user.is_authenticated and request.user.is_marine) or request.user.is_staff or request.user.is_superuser:
        menu_items.append(
        {'title': 'Questions', 'url': reverse('home:questionsint'), 'data_set': False, 'childs': False, 'icon': '<i class="fa-solid fa-question"></i>'},                            
        ) 
    if (request.user.is_authenticated and request.user.is_expert) or request.user.is_staff or request.user.is_superuser:
        menu_items.append(
        {'title': 'Quotations', 'url': reverse('home:quotations'), 'data_set': False, 'childs': False, 'icon': '<i class="fa-brands fa-quora"></i>'},                            
        ) 
        
        menu_items.append(
        {'title': 'Quotations ATG', 'url': reverse('home:quotationsatg'), 'data_set': False, 'childs': False, 'icon': '<i class="fa-solid fa-table-list"></i>'},                            
        ) 
        
    if (request.user.is_authenticated and request.user.is_producer) or request.user.is_staff or request.user.is_superuser:
        menu_items.append(
        {'title': 'All Reports', 'url': reverse('home:all_reports'), 'data_set': False, 'childs': False, 'icon': '<i class="fa-solid fa-list-check"></i>'},                            
        ) 
        
    menu_items.append(
        {'title': 'Settings', 'url': reverse('home:user_settings'), 'data_set': False, 'childs': False, 'icon':'<i class="fa-solid fa-gears"></i>'},                            
        ) 
    
    
    crm_child = [
        {'title':'Lead', 'url': reverse('crm:leads'),'data_set': False, 'childs': False, 'icon': '<i class="fa-solid fa-chalkboard-user"></i>'}
    ] 
    
    if request.user.is_staff or request.user.is_superuser:
        menu_items.append(
        {'title': 'CRM', 'url': '#', 'data_set': False, 'childs': crm_child, 'icon': '<i class="fa-brands fa-leanpub"></i>'},                            
        )  
        
    menu_items.append(
        {'title': 'Profile', 'url': reverse('accounts:user_link'), 'data_set': False, 'childs': False, 'icon' : '<i class="fa-solid fa-user-tie"></i>'},                            
        ) 
        
        
    
    
    return menu_items
    

def header_menus(request):    
    
    menu_items = []
    
    
    menu_items.append(
        {'title': 'About', 'url': '/#about', 'data_set': False},                            
        )  
    menu_items.append(            
        {'title': 'Blogs', 'url': reverse('blog:post_list'), 'data_set': False},                                
        ) 
    menu_items.append(                 
        {'title': 'Glossary', 'url': reverse('glossary:g_list'), 'data_set': False},                   
        ) 
    
    
    
    if (request.user.is_authenticated and request.user.is_producer) or request.user.is_staff or request.user.is_superuser:         
        menu_items.insert(2,     
            {'title': 'Evaluation', 'url': reverse('evaluation:evaluation2'), 'data_set': False},    
            ) 
        
        
        
    
    return menu_items

def account_menus(request):
    menu_items = []    
   
    if request.user.is_authenticated:
        menu_items.append(
            {'title': 'Dashboard', 'url': reverse('home:dashboard'), 'data_set': False},                            
            )  
        menu_items.append(
            {'title': 'Profile', 'url': reverse('accounts:user_link'), 'data_set': False},                            
            )         
        menu_items.append(
            {'title': 'Log Out', 'url': reverse('logout'), 'data_set': False},                            
            ) 
    else:
        menu_items.append(
            {'title': 'Login', 'url': reverse('login'), 'data_set': False},                            
            ) 
        menu_items.append(
            {'title': 'Signup', 'url': '/#register', 'data_set': False},                            
            ) 
        menu_items.append(
            {'title': 'Reset Password', 'url': reverse('password_reset'), 'data_set': False},                            
            ) 
        
    if (request.user.is_authenticated and request.user.is_expert) or request.user.is_staff or request.user.is_superuser:
        menu_items.insert(4,
            {'title': 'My Service', 'url': reverse('partner_service', args=[request.user.id]), 'data_set': False},                            
            ) 
        
    return menu_items
        
        
    
