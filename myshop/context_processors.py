from cart.cart import Cart
from cart.models import CartUser
from profileUser.models import User


def cart(request):
    return {'cart': CartUser.objects.get(user=request.user)} if request.user.is_authenticated else {'cart': Cart(request)}


def users(request):
    return {'all_users': list(User.objects.values_list("username", flat=True))}
