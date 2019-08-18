from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
import os

from cart.models import CartUser
from cart.cart import Cart
from .models import *
from .forms import *


class ProductList(ListView):
    
    def get(self, request, **kwargs):
        category = kwargs.get('category')
        if category:
            category = Category.objects.get(name=category)
            products = Product.objects.filter(categories=category)
        else: 
            products = Product.objects.all()

        products = products.order_by('-ratings__average')

        context = {
                'category': category,
                'products': products,
                }
        return render(request, 'product/list.html', context=context)
  


class ProductDetail(DetailView):

    def get(self, request, username, slug):
        product = get_object_or_404(Product, author__username=username, slug=slug)
        images = ProductImage.objects.filter(product=product)
        error = None
        if request.user.is_authenticated:
            cart = CartUser.objects.get(user=request.user).products.values_list('id', flat=True)
            if product.id in cart:
                error = 'Товар уже в корзине'
        else:
            cart = Cart(request)
            if str(product.id) in cart.all():
                error = 'Товар уже в корзине'

        context = {
                'product': product,
                'images' : images,
                'error'  : error
                }
        return render(request, 'product/detail.html', context=context) 


class ProductAdd(LoginRequiredMixin, FormView):

    def get(self, request, **kwargs):
        form = ProductForm()
        form_images = ImagesFormSet()
        return render(request, 'product/create.html', context={'form': form, "form_images": form_images})

    def post(self, request, **kwargs):
        error = ''
        form = ProductForm(request.POST, request.FILES)
        form_images = ImagesFormSet(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['name'] not in Product.objects.filter(author=request.user).values_list('name', flat=True):
                if form_images.is_valid():
                    if self.is_preview(form_images.cleaned_data):
                        product = Product.objects.create(
                                                      author=request.user,
                                                      name=form.cleaned_data['name'],
                                                      description=form.cleaned_data['description'],
                                                      price=form.cleaned_data['price']
                                                      )
                        data_file = form.cleaned_data['file'].read() 
                        product.file.save(form.cleaned_data['file'].name, ContentFile(data_file))
                        try:
                            os.makedirs('%suser_products/%s/%s/file/' % (settings.MEDIA_ROOT, product.author.username, product.name))
                        except:
                            pass

                        new_path = '%suser_products/%s/%s/file/%s' % (settings.MEDIA_ROOT, product.author.username, product.name, product.file.name)
                        os.rename(product.file.path, new_path)
                        new_path = '/user_products/%s/%s/file/%s' % (product.author.username, product.name, product.file.name)
                        product.file.name = new_path
                        product.save()


                        for cat in form.cleaned_data['categories']:
                            product.categories.add(Category.objects.get(name=cat))

                        for f in form_images.cleaned_data:
                            if len(f) > 0:
                                data = f['images'].read() #Если файл целиком умещается в памяти
                                photo = ProductImage(product=product)
                                photo.image.save(f['images'].name, ContentFile(data))
                                photo.preview = f['preview']
                                photo.save()
                                
                                new_path = '%suser_products/%s/%s/%s' % (settings.MEDIA_ROOT, photo.product.author.username, photo.product.name, photo.image.name)
                                os.rename(photo.image.path, new_path)
                                new_path = '/user_products/%s/%s/%s' % (photo.product.author.username, photo.product.name, photo.image.name)
                                photo.image.name = new_path
                                photo.save()

                        return redirect(product)
                    else:
                        error = 'Выберите титульное фото'
                else:
                    error = 'Выберите хотя бы одно фото'
            else:
                error = 'У вас уже есть товар с таким названием'
        else:
            error = form.errors #'Слишком большая сумма'
        print(error)
        return render(request, 'product/create.html', context={'form': form, "form_images": ImagesFormSet, 'error': error})

    def is_preview(self, form):
        prev_count = 0
        for f in form:
            if len(f) > 0:
                if f['preview']:
                    prev_count += 1

        if prev_count > 0:
            return True
        return False





