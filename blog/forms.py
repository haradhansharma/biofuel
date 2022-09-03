from django import forms
from django.forms import fields
from .models import *

        
# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         # fields = '__all__' 
#         fields = [
#             "title",
#             "image",            
#             "body",
#             "tags",
#             "status",
#         ]