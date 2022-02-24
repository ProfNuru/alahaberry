from products.models import Product, ProductHit, Categorie, Order, Damage
from users.models import Profile, AlahaBerrySetting, Discount
from ads.models import Advertisement
from .models import Slide

def extras(request):
	context = {
		'app_setting': AlahaBerrySetting.objects.last(),
		'discount': Discount.objects.last(),
		'categories': Categorie.objects.all(),
		'recent_sales': Order.objects.all().order_by('-id')[:3],
		'all_products': Product.objects.all().order_by('?'),
		'featured_products': Product.objects.filter(featured=True).order_by('?'),
		'top_picks': ProductHit.objects.select_related('product').all().order_by('-views')[:10]
	}
	return context

	