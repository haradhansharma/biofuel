from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from .forms import UserCreationForm, UserChangeForm
from .models import User, UserType, Profile, UsersNextActivity
from django.contrib import messages
from django.utils.translation import ngettext
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False     

# This is a placeholder comment that indicates not to modify the code below.
'''***DO not change anything here in this file.'''

class UserAdmin(UserAdmin):
    """
    Custom UserAdmin class to configure the admin interface for User model.
    """
    
    add_form = UserCreationForm    # Using custom UserCreationForm for adding users.
    form = UserChangeForm         # Using custom UserChangeForm for editing users.
    inlines = [ProfileInline]     # Display ProfileInline in the UserAdmin page.
   
    list_display = ['usertype', 'experts_in', 'phone', 'email', 'username', 'is_staff', 'is_active', 'email_verified',]
    # Display these fields in the list view of UserAdmin.
    
    list_filter = ('usertype', 'is_active', 'is_staff', 'experts_in', 'email_verified',)
    # Enable filtering based on these fields in the right sidebar.
    
    search_fields = ('email', 'phone', 'orgonization', 'username', 'experts_in', 'email_verified', )
    # Enable searching for users using these fields.
    
    fieldsets =  (
        (None, {'fields': ('usertype',  'experts_in', 'phone', 'orgonization',)}),
    ) + UserAdmin.fieldsets 
    # Customize the layout of the user editing page.
    
    ordering = ('-date_joined',)
    # Order users by their date of joining.
    
    @admin.action(description='Activate selected account and send mail')
    def activate_account(self, request, queryset):
        """
        Custom admin action to activate selected user accounts and send activation emails.
        """
        updated = queryset.update(is_active= True)
        self.message_user(request, ngettext(
            '%d User was successfully marked as active.',
            '%d Users were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)
        for user in queryset:
            user.send_active_mail(request)
     
    @admin.action(description='Deactivate selected account')
    def deactivate_account(self, request, queryset):
        """
        Custom admin action to deactivate selected user accounts.
        """
        updated = queryset.update(is_active= False)
        self.message_user(request, ngettext(
            '%d User was successfully marked as deactive.',
            '%d Users were successfully marked as deactive.',
            updated,
        ) % updated, messages.SUCCESS)
        
    @admin.action(description='Send mail to the selected Marine Expert to update feedback ')
    def send_mail_to_expert(self, request, queryset):
        """
        Custom admin action to send courtesy emails to selected Marine Experts.
        """
        user_type = []
        for i in queryset:
            user_type.append(i.usertype.is_marine)
        if False in user_type:
            return self.message_user(request, "Non Marine Expert Selected! Please select Marine experts only!")      
        
        
        current_site = Site.objects.get_current()
        subject = 'Question updated!'    
        message = render_to_string('emails/expert_mail.html', {                        
            'domain': current_site.domain,            
            })  
        mail_to_expert = [(subject, message, '', [obj.email]) for obj in queryset]
        send_mass_mail((mail_to_expert), fail_silently=False) 
        self.message_user(request, "Mail sent successfully ")
        
    actions = [activate_account, deactivate_account, send_mail_to_expert]
    # Include the custom actions in the admin actions dropdown.
    
admin.site.register(User, UserAdmin)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for UserType model.
    """
    list_display = [f.name for f in UserType._meta.fields if f.editable and not f.name == "id"] 
    # Display the fields of UserType model in the admin list view.
    
    list_filter = ('name', )
    # Enable filtering UserType objects based on their names.
    
    search_fields = ('name', )
    # Enable searching for UserType objects using their names.
    
    prepopulated_fields = {'slug': ('name',)}   
    # Automatically populate the 'slug' field based on the 'name' field.
    
    ordering = ('name',)
    # Order UserType objects by their names.
    
admin.site.register(UsersNextActivity)

    