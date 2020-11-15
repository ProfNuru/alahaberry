from django.contrib import admin
from .models import (Categorie, Product, Damage, Order, ProductHit)


admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Damage)
admin.site.register(Order)
admin.site.register(ProductHit)

