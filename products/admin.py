from django.contrib import admin
from .models import (Categorie, Product, Damage, 
					Order, ProductHit, ItemRequest, 
					SoldItem, ItemColor)


admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Damage)
admin.site.register(Order)
admin.site.register(ProductHit)
admin.site.register(ItemRequest)
admin.site.register(SoldItem)
admin.site.register(ItemColor)

