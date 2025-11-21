import uuid
from django.db import models


# 職員（管理者）テーブル
class Staff(models.Model):
    # 職員ID
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 氏名
    name = models.CharField(max_length=100, verbose_name="氏名")
    # パスワード
    password = models.CharField(max_length=100, verbose_name="パスワード")




# 観光地テーブル
class Spot(models.Model):
    # 観光地ID
    spot_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    # 観光地名称
    spot_name = models.CharField(max_length=100, verbose_name="観光地名称")
    # 住所
    address = models.CharField(max_length=200, verbose_name="住所")
    # カテゴリ
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # 説明
    explanation = models.TextField(max_length=2000, verbose_name="説明")
    # 営業時間
    business_hours = models.CharField(max_length=100, verbose_name="営業時間")
    # 定休日
    regular_holiday = models.CharField(max_length=100, verbose_name="定休日")
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    # 地区
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.spot_name