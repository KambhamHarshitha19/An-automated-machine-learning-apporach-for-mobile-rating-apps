from django import  forms
from .models import UserRegisterModel

class UserRegisterForm(forms.ModelForm):
     Name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control' , 'pattern' : '[a-zA-Z]+'})), required=True , max_length=30)
     Username = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control' ,'pattern' : '[a-zA-Z]*'})) , required=True , max_length=30)
     Password = forms.CharField(widget=(forms.PasswordInput(attrs={'class' : 'form-control' , 'pattern' :'(?=.*\d)(?=.[a-z])(?=.*[A-Z]).{8,}','title':'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'})) , required=True , max_length=30) 
     Email = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control', 'pattern' : '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'})) , required=True , max_length=30)
     Phone_No = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control ' , 'patter':'[56789][0-9]{9}' })) , required=True , max_length=10)
     Locality = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control', 'pattern':'[a-zA-Z]+'})) , required=True , max_length=30)
     State = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control' , 'pattern':'[a-zA-Z]+'})) , required=True , max_length=30)
     Address = forms.CharField(widget=(forms.TextInput(attrs={'class' : 'form-control' , 'pattern':'[a-zA-Z]+'})) , required=True , max_length=30)
     status = forms.CharField(widget=(forms.HiddenInput(attrs={'class' : 'form-control'}  ) )  , initial='waiting')
     class Meta:
         model = UserRegisterModel
         fields = '__all__'