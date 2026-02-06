from django.contrib import admin
from .models import Spot
from .models import Events
from .models import Profile


admin.site.register(Spot)
admin.site.register(Events)
admin.site.register(Profile)