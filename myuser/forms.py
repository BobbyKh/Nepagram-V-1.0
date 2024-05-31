from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    
def clean_email(self):
    data = self.cleaned_data["email"]
    
    if not data:
        raise forms.ValidationError("Email is required")
    
    return data



