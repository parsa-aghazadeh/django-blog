from django import forms

class PostFrom(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea)
    
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea,max_length=40)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=40)    
    
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=40)
    email    = forms.EmailField(max_length=50)
    password_confirmation = forms.CharField(max_length=40)
    
    
    
    
class UserInputForm(forms.Form):
    input_field = forms.CharField(label="نام کاربری یا ایمیل",
                                  widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری یا ایمیل خود را وارد کنید'}))

    
# class ForgetPasswordForm(forms.Form):
#     email_or_username = forms.EmailField(max_length=60)
    