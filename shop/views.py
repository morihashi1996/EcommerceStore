from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def categories(request):
    return {'categories': Category.objects.all()}


def all_products(request):
    products = Product.products.all()
    return render(request, 'shop/products.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'shop/product-detail.html', {'product': product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category.html', {'category': category, 'products': products})
