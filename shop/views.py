from django.shortcuts import render

# Create your views here.

def shop(request, *args, **kwargs):
    """ Vue des produits"""
    context = {}
    return render(request, "../templates/shop/index.html", context)