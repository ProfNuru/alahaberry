from products.models import Product, Categorie, Order, Damage
from users.models import Profile, AlahaBerrySetting, Discount
from ads.models import Advertisement

def extras(request):
	context = {
		'app_setting': AlahaBerrySetting.objects.last(),
		'discount': Discount.objects.last(),
		'categories': Categorie.objects.all(),
		'recent_sales': Order.objects.all().order_by('-id')[:3],
		'recent_products': Product.objects.all().order_by('-id')[:3],
		'featured_products': Product.objects.filter(featured=True).order_by('-id')[:3],
		'vertical_ads': Advertisement.objects.filter(vertical=True)
	}
	return context

	