from django.contrib import admin
from .models import Event  # イベントモデル読み込み

# ===============================
# 管理画面に Event モデルを表示
# ===============================
admin.site.register(Event)
