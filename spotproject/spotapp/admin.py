from django.contrib import admin

from .models import Spot,Events,Profile,Review,Favorite,Category,District
from spotapp_admin.models import  Osirase

admin.site.register(Spot)
admin.site.register(Events)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Category)
admin.site.register(District)
admin.site.register(Osirase)
