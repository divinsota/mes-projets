# Mini-Projet Cinéma

## Description
Ce projet est une application web pour un cinéma d’un petit village. Elle permet aux clients de voir les films disponibles et à l’affiche.  
Le site utilise l’API OMDb pour récupérer les informations des films (titre, poster, résumé, acteurs, genre, notes, etc.) et est développé en HTML, CSS et JavaScript.  
Le site est responsive et conçu pour être facile à utiliser.

## Fonctionnalités
- **Page d’accueil (index.html)** : films tendances (minimum 3), avec poster, titre et lien vers la page détails.
- **Page de recherche (search.html)** : barre de recherche en temps réel, affichage des résultats avec poster, titre et lien vers la page détails, bouton pour charger plus de résultats.
- **Page détails d’un film (movie.html)** : affiche titre, poster, résumé complet, genre, acteurs et, en bonus, notes et date de sortie DVD.

## Technologies
- HTML5
- CSS3
- JavaScript (ES6+)
- API OMDb
- Serveur HTTP pour tester localement (Live Server ou NPM serve)

## Organisation
- `index.html` : page d’accueil
- `search.html` : page recherche
- `movie.html` : page détails
- `css/style.css` : styles
- `js/index.js` : script pour index.html
- `js/search.js` : script pour search.html
- `js/movie.js` : script pour movie.html
- `README.md` : ce fichier

## Utilisation
1. Cloner ou télécharger le repository
2. Lancer un serveur HTTP (Live Server ou NPM serve)
3. Ouvrir `index.html` dans un navigateur
4. Explorer les pages et fonctionnalités

## Bonnes pratiques
- Code segmenté par page
- Interface responsive (mobile-first)
- Accessibilité respectée
- Git bien géré (branches et commits clairs)
- Fonctionnalité “Charger plus de films” pour une meilleure UX

## Bonus
- Affichage des notes et dates de sortie DVD
- Amélioration de l’interface et des animations
- Documentation de l’API OMDb pour futures mises à jour
