from django import forms

class urlForm(forms.Form):
    url = forms.URLField(required=True, 
    widget=forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Enter your URL here', 'aria-describedby':"button-addon2"}))