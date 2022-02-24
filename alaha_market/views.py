from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core import serializers
from django.utils.safestring import mark_safe
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from products.models import Product, Categorie, Order, Damage, ItemRequest, SoldItem, ItemColor, ProductHit
from users.models import Profile, AlahaBerrySetting
from customers.models import Subscriber
from ads.models import Advertisement
from .models import Slide
from .forms import CreateOrderForm, SubscriberForm, RequestForm, SoldItemForm
from itertools import chain

import random
import datetime
import pytz
import json
import decimal


def privacy_policy(request):
	return render(request,'alaha_market/privacy_policy.html')


def terms_of_service(request):
	return render(request, 'alaha_market/terms.html')


def homepage(request):
	if request.GET.get('search-field'):
		search_term = request.GET.get('search-field').strip()
		search_keywords = search_term.split(" ")

		list_of_querysets = []
		for term in search_keywords:
			list_of_querysets.append(Product.objects.filter(Q(product_name__icontains=term)|Q(product_desc__icontains=term)|Q(tags__icontains=term)))
		
		search_results = list(chain(*list_of_querysets))
		
		context = {
			'search_results': search_results,
			'number_of_results': len(search_results)
		}
		print("Search request:", context)
		return render(request, 'alaha_market/search_results.html', context)

	context = {
		'slides': Slide.objects.all().order_by('?')[:3]
	}
	print("Homepage slides:",context)
	return render(request, 'alaha_market/homepage.html', context)


def initialize_page(request):
	print("Making AJAX request for products")
	if request.is_ajax():
		products = Product.objects.select_related('category').all().order_by('?')
		# product_hits = ProductHit.objects.all().order_by('-views')[:10]

		# serialized_product_hits = serializers.serialize('json', product_hits)

		serialized_products = serializers.serialize('json', products)
		print("Sending storage products:", serialized_products)
		return JsonResponse(serialized_products, safe=False, status=200)
	return redirect('homepage')


def item_damages(request):
	if request.is_ajax():
		item_id = int(request.GET['item_id'])
		product_hits = ProductHit.objects.get(product__id=item_id)
		product_hits.views += 1
		product_hits.save()
		
		damages = Damage.objects.filter(product__id=item_id)
		serialized_damages = serializers.serialize('json', damages)
		return JsonResponse(serialized_damages, safe=False, status=200)

	return redirect('homepage')


def item_colors(request):
	if request.is_ajax():
		item_id = int(request.GET['item_id'])
		colors = ItemColor.objects.filter(product__id=item_id)
		serialized_colors = serializers.serialize('json',colors)
		return JsonResponse(serialized_colors, safe=False, status=200)
	return redirect('homepage')


def all_products(request):
	query = request.GET.get('q')
	category_id = 0
	if request.GET.get('category'):
		category_id = request.GET.get('category')
		
	all_categories = False

	if int(category_id) > 0 and query:
		category = Categorie.objects.get(id=int(category_id))
		products = Product.objects.select_related("seller").filter(Q(product_name__icontains=query)|Q(product_desc__icontains=query)|Q(tags__icontains=query),category=category)
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
	tags = product.tags
	
	context = {
		'title': "Alahaberry | " + product.product_name,
		'product': product,
		'damages': Damage.objects.filter(product=product),
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


def subscribe_to_newsletter(request):
	if request.is_ajax():
		sub_data = {
			'email': request.POST['subscription_email']
		}
		sub_form = SubscriberForm(sub_data)
		if(sub_form.is_valid()):
			sub_form.save()
			return JsonResponse(json.dumps({'subscribed':True}), safe=False, status=200)
	return redirect('homepage')


def get_site_data(request):
	if request.is_ajax():
		site_data = AlahaBerrySetting.objects.all().values_list('application_name','about',
			'address','contact1','contact2','contact3','email','google_map','region','city',
			'facebook_url','instagram_url','twitter_url','google_url','linkedin_url','logo',
			'cover_photo','favicon')
		site_data_list = []
		for i in site_data:
			site_data_dict = {
				'application_name':i[0],
				'about':i[1],
				'address':i[2],
				'contact1':i[3],
				'contact2':i[4],
				'contact3':i[5],
				'email':i[6],
				'google_map':i[7],
				'region':i[8],
				'city':i[9],
				'facebook_url':i[10],
				'instagram_url':i[11],
				'twitter_url':i[12],
				'google_url':i[13],
				'linkedin_url':i[14],
				'logo':i[15],
				'cover_photo':i[16],
				'favicon':i[17]				
			}
			site_data_list.append(site_data_dict)
		return JsonResponse(json.dumps(site_data_list), safe=False, status=200)
	return redirect('homepage')


def submit_order(request):
	if request.is_ajax():
		items_ordered = json.loads(request.POST['order_items'])

		print(items_ordered)

		request_data = {
			'customer_email': request.POST['cust_email'],
			'customer_phone': request.POST['cust_phone'],
			'number_of_items': len(items_ordered),
			'total_amount': request.POST['total_amount']
		}

		request_form = RequestForm(request_data)

		sell_rate = AlahaBerrySetting.objects.last()
		request_success = True
		if request_form.is_valid():
			new_request = request_form.save()
			for item in items_ordered:
				item_amount = float(decimal.Decimal(item['qty']) * decimal.Decimal(item['selected_item']['fields']['product_price']))
				item_ordered = {
					'item': Product.objects.get(id=item['selected_item']['pk']),
					'request': new_request,
					'qty': item['qty'],
					'amount': item_amount,
					'seller_earning': float(decimal.Decimal(item_amount) - (decimal.Decimal(item_amount) * sell_rate.charges_on_sale))
				}

				sold_item_form = SoldItemForm(item_ordered)

				if sold_item_form.is_valid():
					print("Item sold")
					sold_item_form.save()
				else:
					print("Item sale failed!")
					request_success = False
		else:
			request_success = False

		order_feedback = {
			'order_placed': request_success
		}
		return JsonResponse(json.dumps(order_feedback), safe=False, status=200)
	return redirect('homepage')

