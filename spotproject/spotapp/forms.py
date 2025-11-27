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
 
#お問い合わせフォーム
class ContactForm(forms.Form):
    name = forms.CharField(label="ユーザー名")
    email = forms.EmailField(label="メールアドレス")
    message = forms.CharField(widget=forms.Textarea,label="お問い合わせ内容")
 
 