from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Category)
admin.site.register(Commande)
admin.site.register(CommandeArticle)
admin.site.register(AddressChipping)