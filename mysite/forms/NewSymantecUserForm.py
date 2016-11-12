from django import forms

class NewSymantecUserForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=70)
    first_name = forms.CharField(label='First Name', max_length=25, required=False)
    last_name = forms.CharField(label='Last Name', max_length=25, required=False)
    credential_id = forms.CharField(label='Hardware Credential ID (Optional)', max_length=12, required=False)
    security_code = forms.CharField(label='6 Digit Security Code (Optional)', max_length=6, required=False)
    phone_number = forms.CharField(label='Phone Number (Optional)', max_length=11, required=False)
