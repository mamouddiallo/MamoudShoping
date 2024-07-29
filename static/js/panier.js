    // Définition de la fonction getCookie
    function getCookie(name) {
        var cookieArr = document.cookie.split(";");
        for (var i = 0; i < cookieArr.length; i++) {
            var cookiePair = cookieArr[i].split("=");
            if (name == cookiePair[0].trim()) {
                return decodeURIComponent(cookiePair[1]);
            }
        }
        return null;
    }

    // Récupération du panier depuis les cookies
    var panier = JSON.parse(getCookie('panier'));
    if (panier == undefined) {
        panier = {};
        console.log("panier cree");
        document.cookie = "panier=" + JSON.stringify(panier) + ";domain=;path=/";
    }
    console.log(panier);

    // Définition de la fonction addCookieArticle
    function addCookieArticle(produitId, action) {
        console.log("L'utilisateur n'est pas authentifié");

        if (action == "add") {
            if (panier[produitId] == undefined) {
                panier[produitId] = {"qte": 1};
            } else {
                panier[produitId]["qte"] += 1;
            }
        }

        if (action == "remove") {
            panier[produitId]["qte"] -= 1;
            if (panier[produitId]["qte"] <= 0) {
                delete panier[produitId];
            }
        }
        console.log('panier mis à jour');
        document.cookie = 'panier=' + JSON.stringify(panier) + ";domain=;path=/";
        location.reload()
    }

    // Attacher les écouteurs d'événements aux boutons de mise à jour du panier
    var produitBtns = document.getElementsByClassName('update-panier');
    for (var i = 0; i < produitBtns.length; i++) {
        produitBtns[i].addEventListener('click', function() {
            var produitId = this.dataset.produit;
            var action = this.dataset.action;

            if (user === "AnonymousUser") {
                addCookieArticle(produitId, action);
            } else {
                updateUserCommande(produitId, action);
            }
        });
    }

    // Définition de la fonction updateUserCommande
    function updateUserCommande(produitId, action) {
        var url = 'update_article/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ "produit_id": produitId, "action": action })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('data', data);
            location.reload();
        })
        .catch((error) => {
            console.error('There was a problem with your fetch operation:', error);
        });
    }