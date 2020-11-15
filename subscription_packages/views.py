from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView

from users.decorators import allowed_users
from .models import SubscriptionPackage
from .forms import SubscriptionPackageForm


@login_required
@allowed_users(allowed_roles=['admins'])
def all_packages(request):
	if request.method == 'POST':
		sub_package_form = SubscriptionPackageForm(request.POST)
		if sub_package_form.is_valid():
			sub_package_form.save()
			
			messages.success(request, f'New Subscription Package added!')
			return redirect('all-packages')
	sub_package_form = SubscriptionPackageForm()

	context = {
		'all_packages': SubscriptionPackage.objects.all(),
		'sub_package_form': sub_package_form
	}
	return render(request, 'subscription_packages/all_packages.html', context)


@login_required
@allowed_users(allowed_roles=['admins'])
def view_package(request, id):

	context = {
		'package': SubscriptionPackage.objects.get(id=id)
	}
	return render(request, 'subscription_packages/view_package.html', context)



class UpdatePackageView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = SubscriptionPackage
	template_name = 'subscription_packages/package_form.html'
	fields = ['title','cost_per_month','details']
	success_message = "Package edited successfully!"


	def test_func(self):
		group = self.request.user.groups.all()[0].name
		if group in ['admins']:
			return True
		return False


class DeletePackageView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = SubscriptionPackage
	template_name = 'subscription_packages/package_confirm_delete.html'
	context_object_name = 'package'
	success_url = '/staff_dashboard/subscription_packages/'
	success_message = "Package deleted!"
	

	def test_func(self):
		group = self.request.user.groups.all()[0].name
		if group in ['admins']:
			return True
		return False


