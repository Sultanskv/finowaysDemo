from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

# class RegisterClientForm(UserCreationForm):
    
#     class Meta(UserCreationForm.Meta):
#         model = Account
#         fields=['user_id',]
#     def __init__(self, *args, **kwargs):
#         super(RegisterClientForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'

class ClientLogin(forms.Form):
    user_id = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(ClientLogin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class DateInput(forms.DateInput):
    input_type = 'date'
    
    


class Client_SYMBOL_QTYForm(forms.ModelForm):
    class Meta:
        model = Client_SYMBOL_QTY
        fields = '__all__'
    
    
class SymbolForm(forms.ModelForm):
    class Meta:
        model = SYMBOL
        fields = ['user','SYMBOL']


from .models import HelpMessage

class HelpMessageForm(forms.ModelForm):
    class Meta:
        model = HelpMessage
        fields = ['message']
