from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
								DetailView,
								CreateView,
								UpdateView,
								DeleteView)
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.mail import send_mail

import datetime
import pytz

from .models import Product, Order, Categorie, Damage
from users.models import AlahaBerrySetting
from .forms import CreateOrderForm, CreateCategoryForm, CreateProductDamageForm



@login_required
def add_product_images(request,id):
		
	return render(request, 'users/add_product_image.html', context)


@login_required
def all_product_images(request, id):
	
	return render(request, 'users/all_product_images.html', context)


@login_required
def add_product_damage(request, id):
	product = Product.objects.get(id=id)
	if product.seller == request.user or request.user.groups.all()[0].name != 'sellers':
		if request.method == 'POST':
			damage_form = CreateProductDamageForm(request.POST)
			if damage_form.is_valid():
				description = damage_form.cleaned_data.get('description')
				image = request.FILES['image']

				new_damage = Damage(product=product,description=description,image=image)
				new_damage.save()

				messages.success(request, f'Damage added for item: {product.product_uid}')

		else:
			damage_form = CreateProductDamageForm()	

		context = {
			'product':product,
			'damage_form': damage_form,
			'damages': Damage.objects.filter(product=product)
		}

		return render(request, 'products/add_product_damage.html', context)
	else:
		messages.success(request, f'You accessed an unauthorized page!')
		return redirect('staff-dashboard')


@login_required
def edit_damage(request, id):
	damage = Damage.objects.get(id=id)
	if damage.product.seller == request.user or request.user.groups.all()[0].name != 'sellers':
		if request.method == 'POST':
			damage_form = CreateProductDamageForm(request.POST, request.FILES, instance=damage)
			if damage_form.is_valid():
				description = damage_form.cleaned_data.get('description')

				if len(request.FILES) > 0:
					image = request.FILES['image']
					damage.image = image
					damage.description = description
					damage.save()
				else:
					damage.description = description
					damage.save()

				messages.success(request, f'Damage editted for Item: {damage.product.product_uid}')
				return redirect('add-product-damage', id=damage.product.id)

		else:
			damage_form = CreateProductDamageForm(instance=damage)	

		context = {
			'damage':damage,
			'form': damage_form
		}

		return render(request, 'products/edit_product_damage.html', context)
	else:
		messages.success(request, f'You accessed an unauthorized page!')
		return redirect('staff-dashboard')


@login_required
def delete_damage(request, id):
	damage = Damage.objects.get(id=id)
	p_id = damage.product.id
	if damage.product.seller == request.user or request.user.groups.all()[0].name != 'sellers':
		try:
			damage.delete()
			messages.success(request, f'Damage deleted!')
			return redirect('add-product-damage', id=p_id)
		except:
			messages.success(request, f'Failed to delete damage!')
			return redirect('add-product-damage', id=p_id)
	else:
		messages.success(request, f'You accessed an unauthorized page!')
		return redirect('staff-dashboard')



class CategoryDetailView(DetailView):
	model = Categorie
	template_name = 'users/category_detail.html'
	context_object_name = 'category'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context
	

class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Categorie
	template_name = 'users/category_form.html'
	fields = ['category_name','category_image1','category_desc']
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Categorie
	template_name = 'users/category_form.html'
	fields = ['category_name','category_image1','category_desc']
	

class CategoryDeleteView(DeleteView):
	model = Categorie
	template_name = 'users/category_confirm_delete.html'
	context_object_name = 'category'
	success_url = '/staff_dashboard/'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context


class ProductListView(ListView):
	model = Product
	template_name = 'products/product_list.html'
	context_object_name = 'products'
	ordering = ['product_name']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
	model = Product
	template_name = 'products/product_form.html'
	fields = ['product_name','product_desc',
	'brand_new','product_details',
	'category','product_price','product_thumbnail',
	'product_image1','product_image2','product_image3',
	'tags']
	success_message = "Product added successfully! You can edit, delete, view, and add damages to the Item."


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context


	def form_valid(self, form):
		form.instance.seller = self.request.user
		form.instance.product_name = form.instance.product_name.replace('/','-')
		form.instance.product_name = form.instance.product_name.replace('\\','-')
		return super().form_valid(form)


	def test_func(self):
		if self.request.user.is_authenticated:
			return True
		return False


class AdminProductCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
	model = Product
	template_name = 'products/product_form.html'
	fields = ['seller','product_name','product_desc',
	'brand_new','product_details',
	'category','product_price','product_thumbnail',
	'product_image1','product_image2','product_image3',
	'tags']
	success_message = "New Product added!"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context


	def test_func(self):
		group = self.request.user.groups.all()[0].name
		if group in ['admins']:
			return True
		return False


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Product
	template_name = 'products/product_form.html'
	fields = ['product_name',
	'product_desc','brand_new','product_details','category',
	'product_price','featured','discount_percentage','product_thumbnail',
	'product_image1','product_image2','product_image3',
	'tags']
	success_message = "Product editted successfully!"


	def form_valid(self, form):
		form.instance.seller = self.request.user
		return super().form_valid(form)


	def test_func(self):
		product = self.get_object()
		if self.request.user == product.seller:
			return True
		return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Product
	success_url = '/staff_dashboard/'
	success_message = "Item Deleted!"


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['app_setting'] = AlahaBerrySetting.objects.last()
		return context

	
	def test_func(self):
		product = self.get_object()
		if self.request.user == product.seller or self.request.user.groups.all()[0].name == 'admins' or self.request.user.groups.all()[0].name == 'clerks':
			return True
		return False

