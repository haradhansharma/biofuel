from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *



app_name = 'evaluation'


sitemaps = {
    'static': GfvpSitemap,
    'active_users': UserSitemap,   
    'user_types' : UserTypeSitemap,
    'blog_list' : BlogSitemap,
    'HtmlReportitemap' : HtmlReportitemap,
    
}


urlpatterns = [   
    path('evaluation/thanks/', views.thanks, name='thanks'),      
    path('evaluation/report/<str:slug>', views.report, name='report'),  
    path('evaluation/nreport/<str:slug>', views.nreport, name='nreport'),  
    path('evaluation/nreport_pdf/<str:slug>', views.nreport_pdf, name='nreport_pdf'),   
    path('get-glossary/', views.get_glossary, name='get_glossary'),   
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),   

    
      
]

urlpatterns += [
    path('evaluation2/', views.eva_index2, name='evaluation2'), 
    path('evaluation2/option_add/', views.option_add2, name='option_add2'),  
    path('evaluation2/<int:evaluator_id>/<str:slug>', views.eva_question, name='eva_question'),   
    path('evaluation/stdoils/', views.stdoils, name='stdoils'),
    path('vedio_urls/<str:search_term>', views.vedio_urls, name="vedio_urls"),
    path('std_oils_block/<str:slug>', views.std_oils_block, name="std_oils_block"),
    path('quotation_block/<str:slug>', views.quotation_block, name="quotation_block"),
    path('traficlighthori/<str:last_reports>', views.trafic_light_hori, name="traficlighthori"),
    path('fuel-history/<str:last_reports>', views.fuel_history, name="fuel_history"),
    
    
    
    
    
]
