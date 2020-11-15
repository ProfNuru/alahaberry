from django.contrib import admin
from .models import Profile, Subscription, AlahaBerrySetting, Discount


admin.site.register(Profile)
admin.site.register(Subscription)
admin.site.register(AlahaBerrySetting)
admin.site.register(Discount)
