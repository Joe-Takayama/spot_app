from django.forms import ModelForm, TextInput, PasswordInput
from .models import Staff

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'password']
        widgets = {
            'name':TextInput(attrs={
                'placeholder': 'ユーザー名(職員の方は職員名)を入力してください'
            }),
            'password':PasswordInput(attrs={
                'placeholder': 'パスワードを入力してください'
            }),
        }