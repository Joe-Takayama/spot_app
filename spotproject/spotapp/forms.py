from django.forms import ModelForm, TextInput, PasswordInput, Textarea
from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
User = get_user_model()


# ------------------------
# 新規登録フォーム
# ------------------------
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]  # 標準 User に合わせる
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "ユーザー名を入力してください"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "メールアドレスを入力してください"
            }),

        }
        help_texts = {
            "username": "",  # ユーザー名の補助テキストを非表示にする
        }

    # パスワード暗号化
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # ← set_password は標準UserでOK
        if commit:
            user.save()
        return user
    
# プロフィール作成・更新用フォーム
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["icon"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"] 

#プロフィール編集用フォーム
class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # viewから渡す
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ["username"]
        labels = {"username": "変更後のユーザー名"}

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()

        if not username:
            raise ValidationError("ユーザー名を入力してください。")

        # 自分以外で同名がいたらNG（大文字小文字無視）
        qs = User.objects.filter(username__iexact=username)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)

        if qs.exists():
            raise ValidationError("そのユーザー名は既に使われています。")

        return username

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


# ------------------------
# ログインフォーム
# ------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"placeholder": "ユーザー名を入力してください"})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"placeholder": "パスワードを入力してください"})
    )



