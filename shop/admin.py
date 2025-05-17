from django.contrib import admin
from .models import Product
from django.http import HttpResponse
from django.shortcuts import render


# Register your models here.
admin.site.register(Product)