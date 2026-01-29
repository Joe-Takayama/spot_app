import uuid
from django.db import models
from spotapp.models import Spot, Events

# 職員（管理者）テーブル
class Staff(models.Model):
    # 職員ID
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 氏名
    name = models.CharField(max_length=100, verbose_name="氏名")
    # パスワード
    password = models.CharField(max_length=128, verbose_name="パスワード")



# # 地区別テーブル
# class District(models.Model):
#     #地区ID
#     district_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #地区名称
#     district_name = models.CharField(max_length=100, verbose_name="地区名称")

#     def __str__(self):
#          return self.district_name


# # カテゴリテーブル
# class Category(models.Model):
#     # カテゴリID
#     category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     # カテゴリ名称
#     category_name = models.CharField(max_length=100, verbose_name="カテゴリ名称")

#     def __str__(self):
#         return self.category_name


# # 観光地テーブル
# class Spot(models.Model):
#     # 観光地ID
#     spot_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
#     # 観光地名称
#     spot_name = models.CharField(max_length=100, verbose_name="観光地名称")
#     # 住所
#     address = models.CharField(max_length=200, verbose_name="住所")
#     # カテゴリ
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     # 説明
#     explanation = models.TextField(max_length=2000, verbose_name="説明")
#     # 営業時間
#     business_hours = models.CharField(max_length=100, verbose_name="営業時間")
#     # 定休日
#     regular_holiday = models.CharField(max_length=100, verbose_name="定休日")
#     # 登録日
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
#     # 地区
#     district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,verbose_name="地区別")
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
#     def __str__(self):
#         return self.spot_name
    

# class Events(models.Model):
#     # イベントID
#     event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, null=False, blank=False, editable=False)
#     # イベント名称
#     event_name = models.CharField(max_length=255, verbose_name="イベント名称")
#     # 観光地ID
#     spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE, null=True, blank=True)
#     # 開催日
#     event_date = models.DateField(verbose_name="開催日")
#     # 会場
#     venue = models.CharField(max_length=255, verbose_name="会場")
#     # 詳細
#     details = models.TextField(max_length=2000, verbose_name="詳細情報")
#     # 主催者
#     organizer = models.CharField(max_length=255, verbose_name="主催者")
#     # 登録日
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

#     def __str__(self):
#         return self.event_name
    

class Photo(models.Model):
    # 写真ID
    photo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 写真
    image = models.ImageField(upload_to='spotapp_admin/', verbose_name="写真")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="アップロード日時")

    # SpotテーブルとEventsテーブルの両方に紐づけ
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, null=True, blank=True, related_name='spot_photos')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True, blank=True, related_name='event_photos')

    def __str__(self):
        if self.spot:
            return f"{self.spot.spot_name}の写真"
        if self.event:
            return f"{self.event.event_name}の写真"
        return f"未紐づけ写真{self.photo_id}"

class Osirase(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField('Staff', blank=True, related_name='read_osirase')

    def __str__(self):
        return self.title