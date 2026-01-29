import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
 
 
 
RATING_CHOICES = [
    (1, '★1'),
    (2, '★2'),
    (3, '★3'),
    (4, '★4'),
    (5, '★5'),
]
 
 
# 地区別テーブル
class District(models.Model):
    # 地区ID
    district_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 地区名称
    district_name = models.CharField(max_length=100, verbose_name="地区名称")
 
    def __str__(self):
        return self.district_name
 
 
# カテゴリテーブル
class Category(models.Model):
    # カテゴリID
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # カテゴリ名称
    category_name = models.CharField(max_length=100, verbose_name="カテゴリ名称")
 
    def __str__(self):
        return self.category_name
 
 
# 観光地テーブル
class Spot(models.Model):
    # 観光地ID
    spot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 観光地名称
    spot_name = models.CharField(max_length=100, verbose_name="観光地名称")
    # 住所
    address = models.CharField(max_length=200, verbose_name="住所")
    # カテゴリ（Category は下じゃなくて「文字列」で参照する）
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    # 説明
    explanation = models.TextField(max_length=2000, verbose_name="説明")
    # 営業時間
    business_hours = models.CharField(max_length=100, verbose_name="営業時間")
    # 定休日
    regular_holiday = models.CharField(max_length=100, blank=True, null=True, verbose_name="定休日")
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    # 地区
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    # 緯度経度
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
 
    def __str__(self):
        return self.spot_name
 
 
# お気に入り
class Favorite(models.Model):
    # お気に入りid
    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ユーザーid（ForeignKeyでUserに紐づけ）
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 観光地id（Spot は文字列で参照）
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE)
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
 
    def __str__(self):
        return f"{self.user.user_name} - {self.spot}"
 
 
# レビュー
class Review(models.Model):
    # レビューid
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ユーザーid
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 観光地id
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE)
    # 評価（1〜5）
    rating = models.IntegerField(choices=RATING_CHOICES)
    # コメント
    comment = models.TextField()
    # 投稿日
    posted_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.spot} - {self.rating}点"
    

class Events(models.Model):
    # イベントID
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, null=False, blank=False, editable=False)
    # イベント名称
    event_name = models.CharField(max_length=255, verbose_name="イベント名称")
    # 観光地ID
    spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE, null=True, blank=True)
    # 開催期間
    event_start = models.DateField(verbose_name="開催日", null=True, blank=True)
    event_end = models.DateField(verbose_name="終了日", null=True, blank=True)
    # 開催時間
    event_time = models.CharField(max_length=255, verbose_name="開催時間", null=True, blank=True)
    # 会場
    venue = models.CharField(max_length=255, verbose_name="会場")
    # 住所
    address = models.CharField(max_length=255, verbose_name="住所")
    # 詳細
    details = models.TextField(max_length=2000, verbose_name="詳細情報")
    # 主催者
    organizer = models.CharField(max_length=255, verbose_name="主催者")
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    def __str__(self):
        return self.event_name

 
 
# ユーザープロフィール（Django標準Userを拡張）
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='profile_icons/', null=True, blank=True)
 
    def __str__(self):
        return f"Profile: {self.user.username}"
 
 
# User 作成時に Profile を自動作成
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
        
# お知らせ既読管理モデル
class OsiraseRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    osirase = models.ForeignKey("spotapp_admin.Osirase", on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "osirase")
