
# Créez une plateforme pour amateurs de Nutella

It's a school project named "Create a platform for Nutella enthusiasts".

Requirements :
- Python 3.6 or higher
- PostgreSQL 12 or higher

EN (Soon):
...

FR :
La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que [le gras c’est la vie](https://www.youtube.com/results?search_query=le+gras+c%27est+la+vie)).

## Cahier des charges
Lire [le cahier des charges](https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/DAPython_P8/Cahier_des_charges.zip)

## Étapes
### 1 - Planifier votre projet

Découpez votre projet en étapes et sous-étapes en suivant une méthodologie de projet agile que vous adapterez à vos besoins. Remplissez un tableau Trello ou Pivotal Tracker.
 
### 2 - Créer un nouveau projet Django

Créez votre projet, modifiez les réglages par défaut et commencez à le développer fonctionnalité par fonctionnalité.
 
### 3 - La page d’accueil des héros

Intéressez-vous à la page d’accueil de la plateforme.
Vous aurez besoin d’intégrer une librairie externe, Bootstrap, ainsi que jQuery. Structurez bien vos assets !

Puis créez le contenu HTML et mettez en forme l’ensemble grâce à CSS et ses librairies.
 
### 4 - Ça c'est mon espace

Comment votre utilisateur se crée-t-il un compte ?
Certainement grâce à un premier formulaire.
Codez donc la page de création de compte ainsi que le formulaire associé. Installez le module nécessaire pour gérer l’authentification avec Django.

Mettez à jour la barre de menu pour qu’elle affiche une icône “Mon compte” quand l’utilisateur est connecté et une icône “Créer un compte” quand il ne l’est pas.
Puis créez la page “Mon compte” (voir les esquisses dans [le cahier des charges](https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/DAPython_P8/Cahier_des_charges.zip)).
 
### 5 - Search but don't destroy

Ah, la recherche ! Un défi intéressant !

Commencez par parcourir la documentation de l’API Open Food Facts et trouvez comment récupérer les informations de l’aliment recherché.
Puis construisez votre base de données en y intégrant uniquement les éléments nécessaires (le score nutritionnel par exemple).
Enfin, inventez un algorithme qui va chercher dans votre base de données l’aliment qui a un meilleur score nutritionnel à l’aliment demandé mais qui reste dans la même catégorie. Vous pouvez le faire ! Je crois en vous !
Mettez à jour la page d’accueil et le menu pour que le formulaire de recherche soit effectivement fonctionnel.
Créez la page qui affiche les résultats de recherche.
Puis créez la page détaillant les caractéristiques de l’aliment de substitution.
 
### 6 - Des aliments sains dans un corps sain

À présent, plongez dans la fonctionnalité qui permet à l’utilisateur d’enregistrer un produit de substitution en favoris.
Mettez à jour la page qui affiche les résultats de recherche en ajoutant un bouton sous chaque produit.
Puis ajoutez une nouvelle fonctionnalité à Django.
Créez la page Mes Produits, accessible en cliquant sur la carotte dans le menu.

### 7 - Finitions et mise en ligne
Créez la page Mentions Légales et mettez en ligne votre site en utilisant Heroku.
