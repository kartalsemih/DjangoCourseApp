from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms import widgets
from django.contrib import messages 
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'class':'form-control'})
        self.fields['password'].widget = widgets.PasswordInput(attrs={'class':'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username') 

        if username == 'admin':
            messages.add_message(self.request,messages.SUCCESS,'hoş geldin admin')

        return username 
    
    # def confirm_login_allowed(self,user):
    #     if user.username.startswith('s'):
    #         raise forms.ValidationError('bu kullanıcı adı ile login olamazsınız') 

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'class':'form-control'})
        self.fields['username'].widget = widgets.TextInput(attrs={'class':'form-control'})
        self.fields['email'].widget = widgets.EmailInput(attrs={'class':'form-control'}) 
        self.fields['first_name'].widget = widgets.EmailInput(attrs={'class':'form-control'}) 
        self.fields['last_name'].widget = widgets.EmailInput(attrs={'class':'form-control'}) 
        self.fields['email'].required = True




    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email = email).exists():
            self.add_error('email','email daha önce kullanılmış')

        return email
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'