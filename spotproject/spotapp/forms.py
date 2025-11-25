from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

# 新規登録用フォーム
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }


#プロフィール編集用フォーム
class ProfileEditForm(forms.ModelForm):
    """
    プロフィール編集用フォーム
    - ユーザー名
    - パスワード（任意）
    """

    password = forms.CharField(
        label="新しいパスワード",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "変更するパスワードを入力してください"}),
    )

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {
            "username": "変更するユーザー名を入力してください",
        }
