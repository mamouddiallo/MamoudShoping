from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required 
from datetime import datetime
from.utiles import data_cookie, panier_cookie

# Create your views here.

def shop(request, *args, **kwargs):
    """ Vue principale """
    
    # Récupère tous les objets de type Produit depuis la base de données
    produits = Produit.objects.all()
    
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']
    
    # Crée un contexte avec les articles et la commande à passer au template
    context = {
        'produits': produits,
        'nombre_article':nombre_article
    }
   
    
    # Rend le template 'shop/index.html' avec le contexte fourni
    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    """ Affiche le contenu du panier de l'utilisateur connecté. """
    
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']
    
    # Crée un contexte avec les articles et la commande à passer au template
    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article':nombre_article
    }
    
    # Rend le template 'shop/panier.html' avec le contexte fourni
    return render(request, 'shop/panier.html', context)



def commande(request, *args, **kwargs):
    """ 
    Gère la commande d'un utilisateur connecté en récupérant les articles associés à la commande en cours. 
    Si l'utilisateur n'est pas connecté, initialise un panier vide.
    """
    
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']
        
    
    # Crée un contexte avec les articles et la commande à passer au template
    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article':nombre_article
    }
    
    # Rend le template 'shop/commande.html' avec le contexte fourni
    return render(request, 'shop/commande.html', context)



# def update_article(request, *args, **kwargs):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             produit_id = data.get('produit_id')
#             action = data.get('action')
#             print('id', produit_id, 'action', action)
#             return JsonResponse("Article ajouté", safe=False, json_dumps_params={'ensure_ascii': False})
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
def update_article(request, *args, **kwargs):

    data = json.loads(request.body)

    produit_id = data['produit_id']

    action = data['action']

    client = request.user.client

    produit = Produit.objects.get(id=produit_id)

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action == 'add':

        commande_article.quantite += 1

    if action == 'remove':

        commande_article.quantite -= 1

    commande_article.save()

    if  commande_article.quantite <= 0:

        commande_article.delete()        

    return JsonResponse("Article ajouté", safe=False)
def commandeAnonyme(request, data):
    name = data['form']['name']
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']
    
    cookie_panier = panier_cookie(request)
    articles = cookie_panier['articles']
    client, created = Client.objects.get_or_create(
        email = email
    )
    client.name = name
    client.save()
    commande = Commande.objects.create(
        client = client
    )
    
    for article in articles:
        produit = Produit.objects.get(id=article['produit']['pk'])
        
        CommandeArticle.objects.create(
            produit = produit,
            commande = commande, 
            quantite= article['quantite']
        )

    return client, commande
def traitement_commande(request, *args, **kargs):
    
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
    else:
          client, commande = commandeAnonyme(request, data)
    total = float(data['form']['total'])
    commande.transaction_id = transaction_id
    if commande.get_panier_total == total:
        commande.complete = True
    commande.save()
    
    if commande.produit_pysique:

        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse = data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
)

    return JsonResponse("Traitement complet", safe=False)


