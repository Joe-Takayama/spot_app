from django.forms import ModelForm, TextInput, PasswordInput, Textarea
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password

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

#プロフィール編集用フォーム
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "変更後のユーザー名",
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



