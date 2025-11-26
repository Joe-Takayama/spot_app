import uuid
from django.db import models



RATING_CHOICES = [
    (1, '★1'),
    (2, '★2'),
    (3, '★3'),
    (4, '★4'),
    (5, '★5'),
]

# 利用者テーブル
class User(models.Model):
    # ユーザーid
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 名前
    user_name = models.CharField(max_length=100, verbose_name="氏名")
    # メールアドレス
    email = models.EmailField(max_length=255, verbose_name="メールアドレス")
    # パスワード
    password = models.CharField(max_length=128, verbose_name="パスワード")
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")

    def __str__(self):
        return self.user_name


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
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    # 説明
    explanation = models.TextField(max_length=2000, verbose_name="説明")
    # 営業時間
    business_hours = models.CharField(max_length=100, verbose_name="営業時間")
    # 定休日
    regular_holiday = models.CharField(max_length=100, verbose_name="定休日")
    # 登録日
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    # 地区
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.spot_name


# お気に入り
class Favorite(models.Model):
    # お気に入りid
    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ユーザーid（ForeignKeyでUserに紐づけ）
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
