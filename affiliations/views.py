from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils import timezone

from users.decorators import staff_only, allowed_users
from users.forms import UserRegisterForm

from .models import Coupon, Commission
from .forms import AffiliateForm

import datetime
import pytz
import decimal
from dateutil.relativedelta import relativedelta


@login_required
@allowed_users(allowed_roles=['admins'])
def all_affiliates(request):
	context = {
		'coupons': Coupon.objects.filter(user__groups__name__in=['affiliates']),
		'unpaid_commissions': Commission.objects.filter(paid=False).count(),
		'paid_commissions': Commission.objects.filter(paid=True).count(),
		'add_sales_person_form': UserRegisterForm()
	}
	return render(request, 'affiliations/all_affiliates.html', context)


@login_required
@allowed_users(allowed_roles=['admins'])
def admin_add_affiliate(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			username = form.cleaned_data.get('username')
			
			#Assign new user to group
			group = Group.objects.get(name='affiliates')
			new_user.groups.add(group)
			new_user.save()
	
			messages.success(request, f'New Sales Person {username} added!')
			return redirect('all-affiliates')
		else:
			messages.error(request, f'An error occured!')
			return redirect('all-affiliates')
	else:
		messages.error(request, f'Failed to add Sales Person!')
		return redirect('all-affiliates')


@login_required
@allowed_users(allowed_roles=['affiliates'])
def sales_person(request):
	un_paid_commissions = Commission.objects.filter(coupon__user__id=request.user.id, paid=False)
	total_unpaid_commission = 0
	for commission in un_paid_commissions:
		total_unpaid_commission = total_unpaid_commission + commission.commission

	context = {
		'commissions': Commission.objects.filter(coupon__user__id=request.user.id),
		'paid_commissions': Commission.objects.filter(coupon__user__id=request.user.id,paid=True),
		'total_unpaid_commission': total_unpaid_commission
	}
	return render(request,'affiliations/sales_person.html',context)



@login_required
@allowed_users(allowed_roles=['affiliates'])
def sales_commissions(request):
	pass


@login_required
@allowed_users(allowed_roles=['admins'])
def commissions(request, id):
	coupon = Coupon.objects.get(id=id)
	un_paid_commissions = Commission.objects.filter(coupon=coupon, paid=False)
	total_unpaid_commission = 0
	for commission in un_paid_commissions:
		total_unpaid_commission = total_unpaid_commission + commission.commission

	context = {
		'coupon': coupon,
		'commissions': Commission.objects.filter(coupon=coupon),
		'total_unpaid_commission': total_unpaid_commission
	}
	return render(request, 'affiliations/commissions.html', context)


@login_required
@allowed_users(allowed_roles=['admins'])
def edit_coupon_code(request, id):
	if request.method == 'POST':
		current_coupon = Coupon.objects.get(id=id)
		current_coupon.coupon_code = request.POST['coupon_code']
		current_coupon.save()

		messages.success(request, f'Coupon code editted for {current_coupon.user.username}!')
		return redirect('all-affiliates')
	else:
		messages.success(request, f'Failed to edit coupon code!')
		return redirect('all-affiliates')



@login_required
@allowed_users(allowed_roles=['admins'])
def pay_commission(request, cid, aid):
	commission = Commission.objects.get(id=cid)
	commission.paid = True
	commission.save()
	
	return redirect('commissions', id=aid)


@login_required
@allowed_users(allowed_roles=['admins'])
def pay_all_commissions(request, aid):
	coupon = Coupon.objects.get(id=aid)
	commissions = Commission.objects.filter(coupon=coupon)
	
	for commission in commissions:
		commission.paid = True
		commission.save()
	
	return redirect('commissions', id=aid)


@login_required
def be_an_affiliate(request, id):
	seller = User.objects.get(id=id)
	coupon = Coupon.objects.get(user=seller)
	current_datetime = datetime.datetime.now(tz=pytz.UTC)
	sub_delta = relativedelta(months=1)
	coupon.expiry_date = current_datetime + sub_delta
	coupon.save()

	messages.success(request, f'Thank you for joining our affiliates. Invite more Sellers with your User name and earn on each subscription!')
	return redirect('user-dashboard')

