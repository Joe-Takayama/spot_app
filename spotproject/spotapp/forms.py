from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

# 新規登録用フォーム
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # パスワード暗号化
        if commit:
            user.save()
        return user

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


# ④ ✨イベント登録・編集フォーム 
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'url', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 2025年3月1日〜3日'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
