from django import forms

class SixDigitForm(forms.Form):
    six_digit_code = forms.CharField(label='Six Digit Code', max_length=6)
