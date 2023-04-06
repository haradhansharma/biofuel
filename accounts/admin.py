from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from .forms import UserCreationForm, UserChangeForm
from .models import User, UserType, Profile, UsersNextActivity
from django.contrib import messages
from django.utils.translation import ngettext

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False  
    


'''***DO not change anything here in this file.'''

class UserAdmin(UserAdmin):
    
    
    #taking charge of default Django form.
    add_form = UserCreationForm   
    
    #taking charge of default Django form.
    form = UserChangeForm   
    inlines = [ProfileInline]    
    # model = User
    list_display = ['usertype', 'experts_in', 'email', 'username', 'is_staff', 'is_active', 'email_verified',]    
    list_filter = ('usertype', 'is_active', 'is_staff', 'experts_in', 'email_verified',)
    search_fields = ('email', 'phone', 'orgonization', 'username', 'experts_in', 'email_verified', )
    
    fieldsets =  (
        (None, {'fields': ('usertype', 'experts_in','orgonization',)}),
    ) + UserAdmin.fieldsets 
    ordering = ('-date_joined',)
    
    
    # Creating custom action for admin to activate user account and send mail    
    @admin.action(description='Activate selected account and send mail')
    def activate_account(self, request, queryset):
        updated = queryset.update(is_active= True)
        self.message_user(request, ngettext(
            '%d User was successfully marked as active.',
            '%d Users were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)
        for user in queryset:
            user.send_active_mail(request)
     
     
    # Creating custom action for admin to deactivate user account and send mail     
    @admin.action(description='Deactivate selected account')
    def deactivate_account(self, request, queryset):
        updated = queryset.update(is_active= False)
        self.message_user(request, ngettext(
            '%d User was successfully marked as deactive.',
            '%d Users were successfully marked as deactive.',
            updated,
        ) % updated, messages.SUCCESS)
        
        
    # Creating custom action for admin to send curtesy mail to expert. It is sending massmail using one connection.       
    @admin.action(description='Send mail to the selected Marine Expert to update feedback ')
    def send_mail_to_expert(self, request, queryset):
        user_type = []
        for i in queryset:
            user_type.append(i.usertype.is_marine)
        if False in user_type:
            return self.message_user(request, "Non Marine Expert Selected! Please select Marine experts only!")      
        
        from django.template.loader import render_to_string
        from django.core.mail import send_mass_mail
        current_site = Site.objects.get_current()
        subject = 'Question updated!'    
        message = render_to_string('emails/expert_mail.html', {                        
            'domain': current_site.domain,            
            })  
        mail_to_expert = [(subject, message, '', [obj.email]) for obj in queryset]
        send_mass_mail((mail_to_expert), fail_silently=False) 
        self.message_user(request, "Mail sent successfully ")
        
    actions = [activate_account, deactivate_account, send_mail_to_expert]
admin.site.register(User, UserAdmin)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserType._meta.fields if f.editable and not f.name == "id"] 
    list_filter = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}   
    ordering = ('name',)
    
    
admin.site.register(UsersNextActivity)
    