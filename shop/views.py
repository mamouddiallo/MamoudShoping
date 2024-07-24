from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required 

# Create your views here.

def shop(request, *args, **kwargs):
    """ Vue principale """
    
    # Récupère tous les objets de type Produit depuis la base de données
    produits = Produit.objects.all()
     # Vérifie si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupère l'objet client associé à l'utilisateur connecté
        client = request.user.client
        
        # Récupère ou crée une commande pour le client qui n'est pas encore complétée
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        # Récupère tous les articles associés à la commande en cours
        nombre_article = commande.get_panier_article 
    else:
        # Si l'utilisateur n'est pas connecté, initialise une liste d'articles vide
        articles = []
        
        # Initialise un dictionnaire pour représenter une commande vide
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0
        }
        nombre_article = commande['get_panier_article']
    
    # Crée un contexte avec les articles et la commande à passer au template
    context = {
        'produits': produits,
        'nombre_article':nombre_article
    }
    
    # Crée un dictionnaire de contexte contenant la liste des produits
   
    
    # Rend le template 'shop/index.html' avec le contexte fourni
    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    """ Affiche le contenu du panier de l'utilisateur connecté. """
    
    # Vérifie si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupère l'objet client associé à l'utilisateur connecté
        client = request.user.client
        
        # Récupère ou crée une commande pour le client qui n'est pas encore complétée
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        # Récupère tous les articles associés à la commande en cours
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article 

    else:
        # Si l'utilisateur n'est pas connecté, initialise une liste d'articles vide
        articles = []
        
        # Initialise un dictionnaire pour représenter une commande vide
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0
        }
        nombre_article = commande['get_panier_article']
    
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
    
    # Vérifie si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupère l'objet client associé à l'utilisateur connecté
        client = request.user.client
        
        # Récupère ou crée une commande pour le client qui n'est pas encore complétée
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        # Récupère tous les articles associés à la commande en cours
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article 
    else:
        # Si l'utilisateur n'est pas connecté, initialise une liste d'articles vide
        articles = []
        
        # Initialise un dictionnaire pour représenter une commande vide
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0
        }
        nombre_article = commande['get_panier_article']
    
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


