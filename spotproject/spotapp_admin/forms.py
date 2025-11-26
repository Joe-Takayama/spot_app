from django.forms import ModelForm, TextInput, PasswordInput, Textarea
from .models import Staff, Events, Photo, Spot
from django import forms

#職員ログインフォーム
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

# イベント登録フォーム
class EventCreateForm(ModelForm):
    class Meta:
        model = Events
        fields = ['event_name', 'event_date', 'venue', 'details', 'organizer']
        widgets = {
            'event_name': TextInput(attrs={
                'placeholder': 'イベント名称を入力してください'
            }),
            'event_date': TextInput(attrs={
                'placeholder': '日時を入力してください'
            }),
            'venue': TextInput(attrs={
                'placeholder': '会場を入力してください'
            }),
            'deteils': Textarea(attrs={
                'placeholder': '詳細情報を入力してください'
            }),
            'organizer': TextInput(attrs={
                'placeholder': '主催者を入力してください'
            }),
        }

# 写真登録
class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        labels = {'image': '写真を登録してください'}

class SpotCreateForm(ModelForm):
    class Meta:
        model = Spot
        fields = ['spot_name', 'spot-address', 'spot-time', 'Admission fee', 'etailed information']
        widgets = {
            'spot_name': TextInput(attrs={
                'placeholder': '観光地名称を入力してください'
            }),
            'spot-address': TextInput(attrs={
                'placeholder': '住所を入力してください'
            }),
            'spot-time': TextInput(attrs={
                'placeholder': '営業時間を入力してください'
            }),
            'Admission fee': Textarea(attrs={
                'placeholder': '入場料を入力してください'
            }),
            'etailed information': TextInput(attrs={
                'placeholder': '詳細情報を入力してください'
            }),
        }