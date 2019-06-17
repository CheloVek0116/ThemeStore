from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart


@require_POST
def CartAdd(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	if product_id not in cart.all():
		cart.add(product=product)
	return redirect(product.get_absolute_url())

def CartRemove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:CartDetail')


def CartDetail(request):
	cart = Cart(request)
	return render(request, 'cart/detail.html', {'cart': cart})