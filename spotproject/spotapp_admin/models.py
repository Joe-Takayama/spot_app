import uuid
from django.db import models


# 観光地クラス
class Spot(models.Model):
    # 観光地ID
    spot_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    # 観光地名称
    spot_name = models.CharField(max_length=100, verbose_name="観光地名称")
    # 住所
    addres = models.CharField(max_length=200, verbose_name="住所")
    # カテゴリID
    category_id = models.IntegerField()
    # 説明
    explanation = models.TextField(max_length=2000, verbose_name="説明")
    # 営業時間
    