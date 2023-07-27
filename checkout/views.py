from django.shortcuts import redirect, render
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
# from user.models import CustomUser
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


