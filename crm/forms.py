from django import forms




class UploadLead(forms.Form):
    lead_upload = forms.FileField()