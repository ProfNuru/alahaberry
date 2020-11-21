from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from products.models import Product, Categorie, Order, Damage
from users.models import Profile, AlahaBerrySetting
from customers.models import Subscriber
from ads.models import Advertisement
from .forms import CreateOrderForm

import random
import datetime
import pytz


def privacy_policy(request):
	return render(request,'alaha_market/privacy_policy.html')


def terms_of_service(request):
	return render(request, 'alaha_market/terms.html')


def homepage(request):
	sellers = User.objects.filter(groups__name='sellers', profile__subscription_end__gt=timezone.now())
	horizontal_ads = Advertisement.objects.filter(vertical=False)

	context = {
		'title': "Alahaberry | Buy and Sell anything",
		'home_nav_active': 'activeNav',
		'shops': sellers,
		'products': Product.objects.select_related("seller").all(),
		'popular_products': Product.objects.select_related("seller").filter(seller__profile__subscription_end__gt=timezone.now()),
		'horizontal_ads': horizontal_ads
	}
	return render(request,'alaha_market/homepage.html', context)


def all_products(request):
	query = request.GET.get('q')
	category_id = 0
	if request.GET.get('category'):
		category_id = request.GET.get('category')
		
	all_categories = False

	if int(category_id) > 0 and query:
		category = Categorie.objects.get(id=int(category_id))
		products = Product.objects.select_related("seller").filter(Q(product_name__icontains=query)|Q(product_desc__icontains=query)|Q(tags__icontains=query),category=category)
		print(category)
	elif query:
		category = 'None'
		products = Product.objects.select_related("seller").filter(Q(product_name__icontains=query)|Q(product_desc__icontains=query)|Q(tags__icontains=query))
		all_categories = True
	else:
		category = 'None'
		products = Product.objects.select_related("seller").all()
		all_categories = True


	context = {
		'title': "Alahaberry | Search Results",
		'category': category,
		'products': products,
		'num_of_products': len(products),
		'all_categories': all_categories,
		'query': query
	}
	return render(request, 'alaha_market/all_products.html', context)


def new_products(request):
	products = Product.objects.select_related("seller").filter(brand_new=True)

	context = {
		'title': "Alahaberry | Brand New Items",
		'new_products_nav_active': 'activeNav',
		'products': products,
		'num_of_products': len(products)
	}
	return render(request, 'alaha_market/new_products.html', context)


def used_products(request):
	products = Product.objects.select_related("seller").filter(brand_new=False)

	context = {
		'title': "Alahaberry | Slightly Used Items",
		'used_products_nav_active': 'activeNav',
		'products': products,
		'num_of_products': len(products)
	}
	return render(request, 'alaha_market/used_products.html', context)


def view_product(request, pk, productname):
	product = Product.objects.select_related("seller").get(id=pk, product_name=productname)
	if not request.user.is_authenticated:
		try:
			hit = product.product_hit
			hit.views = hit.views + 1
			hit.last_viewed = timezone.now()
			hit.save()
		except:
			print("No product_hit object for product")

	tags = product.tags
	if request.method == 'POST':
		order_form = CreateOrderForm(request.POST)
		if order_form.is_valid():
			name = order_form.cleaned_data.get('name')
			email = order_form.cleaned_data.get('email')
			phone = order_form.cleaned_data.get('phone')
			order = order_form.cleaned_data.get('order')
			recipient = order_form.cleaned_data.get('recipient')
			closest_landmark = order_form.cleaned_data.get('closest_landmark')
			area = order_form.cleaned_data.get('area')
			house_number = order_form.cleaned_data.get('house_number')


			if product.seller.profile.handle_orders:
				new_order = Order(product=product,name=name,email=email,
							phone=phone,order=order, delivered_by="Shop Owner",
							recipient=recipient, closest_landmark=closest_landmark,
							area=area, house_number=house_number)
				new_order.save()
			else:
				new_order = Order(product=product,name=name,email=email,
							phone=phone,order=order, delivered_by="Alahaberry Sales Persons",
							recipient=recipient, closest_landmark=closest_landmark,
							area=area, house_number=house_number)
				new_order.save()


			messages.success(request, f'You have successfully made an order for Item ID: {product.product_uid}')
			return redirect('view-product', pk=pk, productname=productname)
	else:
		order_form = CreateOrderForm()

	context = {
		'title': "Alahaberry | " + product.product_name,
		'product': product,
		'damages': Damage.objects.filter(product=product),
		'order_form': order_form,
		'same_category_products': Product.objects.filter(category=product.category),
		'related_items': Product.objects.filter(Q(product_name__icontains=tags)|Q(product_desc__icontains=tags)|Q(tags__icontains=tags)),
	}
	return render(request, 'alaha_market/view_product.html', context)


def category_view(request, pk):
	category = Categorie.objects.get(id=pk)
	context = {
		'title': "Alahaberry | "+ category.category_name,
		'category': category,
		'products': Product.objects.select_related("seller").filter(category=category)
	}
	return render(request, 'alaha_market/category_page.html', context)


def shops(request, pk, shopname):
	seller = User.objects.select_related("profile").get(id=pk, username=shopname)
	if seller.profile.subscription_end < timezone.now():
		return redirect('all-shops')

	if seller.profile.business_name != 'NA':
		shop_name = seller.profile.business_name
	else:
		shop_name = seller.username

	context = {
		'title': "Alahaberry | " + shop_name,
		'shop': seller.profile,
		'shop_name': shop_name,
		'products': Product.objects.filter(seller=seller)
	}
	return render(request, 'alaha_market/shop_page.html', context)


def all_shops(request):
	sellers = User.objects.select_related("profile").filter(groups__name='sellers', profile__subscription_end__gt=timezone.now())

	context = {
		'title': "Alahaberry | On Sale",
		'shops_nav_active': 'activeNav',
		'sellers': sellers,
		'num_of_sellers': len(sellers)
	}
	return render(request, 'alaha_market/all_shops.html', context)


def subscribe(request):
	if request.method == 'POST':
		email = request.POST['subscriber-email']
		subscription = Subscriber(email=email)
		subscription.save()
		
		context = {
			'title': "Alahaberry | Thank you for subscribing",
			'products': Product.objects.select_related("seller").all().order_by('-id')
		}
		return render(request, 'alaha_market/subscription_complete.html', context)


