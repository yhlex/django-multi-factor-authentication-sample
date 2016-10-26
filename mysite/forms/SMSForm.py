from django import forms

class SMSForm(forms.Form):
    sms_code = forms.CharField(label='SMS Code', max_length=6)

