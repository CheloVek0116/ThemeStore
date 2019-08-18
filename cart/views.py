from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST


from shop.models import Product
from .cart import Cart
from .models import CartUser


@require_POST
def CartAdd(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	if request.user.is_authenticated:
		cart = CartUser.objects.get(user=request.user)
		if product not in cart.products.all():
			cart.products.add(product)
	else:
		cart = Cart(request)
		if product_id not in cart.all():
			cart.add(product=product)
	
	return redirect(product.get_absolute_url())

def CartRemove(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	if request.user.is_authenticated:
		cart = CartUser.objects.get(user=request.user)
		cart.products.remove(product)
	else:
		cart = Cart(request)
		cart.remove(product)
	return redirect('cart:CartDetail')


def CartDetail(request):
	cart = CartUser.objects.get(user=request.user) if request.user.is_authenticated else Cart(request)		
	return render(request, 'cart/detail.html', {'cart': cart})