from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.models import CartUser
from cart.cart import Cart
from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .tasks import OrderCreated
from profileUser.forms import *

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model

USER = get_user_model()


@staff_member_required
def AdminOrderPDF(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	html = render_to_string('orders/order/pdf.html', {'order': order})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
	# weasyprint.HTML(string=html).write_pdf(response,
	#            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
	return response

@staff_member_required
def AdminOrderDetail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'orders/admin/order.html', {'order': order})


def OrderCreate(request):
	if request.user.is_authenticated:
		cart = CartUser.objects.get(user=request.user)

		if request.method == 'POST':
			form = OrderCreateForm(request.POST)
			if form.is_valid():
				order = Order.objects.create(user=request.user)
				for item in cart.products.all():
					OrderItem.objects.create(order=order, product=item,
											 price=item.price,)
				cart.clear()
				# Асинхронная отправка сообщения
				OrderCreated.delay(order.id)
				return redirect('orders:Orders')

		form = OrderCreateForm()
		return render(request, 'orders/create.html')
	return render(request, 'orders/signup&create_order.html', {'form': SignUpForm})


def Orders(request):
	orders = Order.objects.filter(user=request.user)
	return render(request, 'orders/list.html', {'orders': orders})

def OrderDetail(request, order_id):
	order = Order.objects.get(user=request.user, id=order_id)
	error = ''
	if request.method == 'POST':
		if request.user.balance > order.get_total_cost():
			order_items = order.items.all()
			for item in order_items:
				item_price   = item.price - (item.price / 10 )
				item.product.author.balance += item_price
				item.product.author.save()


			order.paid = True
			order.save()
		else:
			error = 'где деньги?'	
			
	return render(request, 'orders/detail.html', {'order': order, 'error': error})




