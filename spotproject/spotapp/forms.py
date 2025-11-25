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
    """プロフィール編集（パスワード欄は無し）"""

    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "変更するユーザー名を入力してください",
        }

# パスワード変更用フォーム
class PasswordChangeOnlyForm(forms.Form):
    """パスワード変更用フォーム（Userとは別管理）"""

    new_password1 = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="新しいパスワード（確認）",
        widget=forms.PasswordInput
    )