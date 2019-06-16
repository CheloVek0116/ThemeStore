from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile

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
                'products': products,
                }
        return render(request, 'product/list.html', context=context)
  


class ProductDetail(DetailView):

    def get(self, request, username, slug):
        product = get_object_or_404(Product, author__username=username, slug=slug)
        images = ProductImage.objects.filter(product=product)
        
        context = {
                'product': product,
                'images': images,
                }
        return render(request, 'product/detail.html', context=context) 


class ProductAdd(LoginRequiredMixin, FormView):

    def get(self, request, **kwargs):
        form = ProductForm()
        form_images = ImagesFormSet()
        return render(request, 'product/create.html', context={'form': form, "form_images": form_images})

    def post(self, request, **kwargs):
        error = ''
        form = ProductForm(request.POST)
        form_images = ImagesFormSet(request.POST, request.FILES)
        if form.is_valid():
            if form_images.is_valid():
                if self.is_preview(form_images.cleaned_data):
                    product = Product.objects.create(
                                                  author=request.user,
                                                  name=form.cleaned_data['name'],
                                                  description=form.cleaned_data['description'],
                                                  price=form.cleaned_data['price']
                                                  )

                    for cat in form.cleaned_data['categories']:
                        product.categories.add(Category.objects.get(name=cat))

                    for f in form_images.cleaned_data:
                        if len(f) > 0:
                            data = f['images'].read() #Если файл целиком умещается в памяти
                            photo = ProductImage(product=product)
                            photo.image.save(f['images'].name, ContentFile(data))
                            photo.preview = f['preview']
                            photo.save()
                            
                            try:
                                os.makedirs('%suser_products/%s/%s/' % (settings.MEDIA_ROOT, photo.product.author.username, photo.product.name))
                            except:
                                pass
                            new_path = '%suser_products/%s/%s/%s' % (settings.MEDIA_ROOT, photo.product.author.username, photo.product.name, photo.image.name)
                            print(photo.image.path, new_path)
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
            error = 'Слишком большая сумма'
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





