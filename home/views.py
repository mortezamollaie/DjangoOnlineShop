from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from bucket import bucket
from django.contrib.auth.mixins import UserPassesTestMixin
from utils import IsAdminUserMixin


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(availble=True)
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/detail.html', {'product':product})


class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        # tasks.delete_object_task.delay(key)
        bucket.delete_object(key)
        messages.success(request, 'your object will be delete soon.', 'info')
        return redirect('home:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        # tasks.download_object_tasks.delay(key)
        bucket.download_object(key)
        messages.success(request, 'your download will start soon.', 'info')
        return redirect('home:bucket')


