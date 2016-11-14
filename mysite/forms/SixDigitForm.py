from django import forms

class SixDigitForm(forms.Form):
    six_digit_code = forms.CharField(label='6 Digit Code', max_length=6)
