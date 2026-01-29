
#  Documentation technique — Projet Yearbook SUPINFO

##  1. Architecture générale du code

Le projet est organisé en plusieurs modules pour garantir une bonne structure et éviter toute variable globale :

```
code_src/
│
├── main.py                # Point d’entrée du programme
├── fonction_csv.py        # Gestion du fichier CSV des étudiants
├── fonction_img.py        # Fonctions de traitement d'image (redimensionnement, flou, badges, NB)
├── fonction_pdf.py        # Génération des pages et export du yearbook en PDF
│
├── data/                  # Données sources : CSV, photos, citations, photo de classe
├── ressources/            # Logo, couleurs, polices, images décoratives
└── output/                # Dossier de sortie : contient le fichier final yearbook.pdf
```

> Remarque :le dossier `output/` est créé automatiquement par le programme s'il n'existe pas. Il contient le fichier final `yearbook.pdf`.

---

##  2. Rôle des sous-programmes

###  `main.py`
C’est le point d’entrée du programme.  
Il :
- Charge les données à partir du CSV via `fonction_csv.py`.
- Appelle la fonction principale `creer_yearbook_pdf()` du module `fonction_pdf.py`.
- Définit les options globales (format, noir et blanc, citations, etc.).
- Génère le fichier final `output/yearbook.pdf`.

---

###  `fonction_csv.py`
Contient une seule fonction principale :

```python
charger_etudiants(fichier_csv)
```
Rôle :  
Lire le fichier CSV des étudiants et retourner une liste de dictionnaires contenant :
- `id`, `prenom`, `nom`
- `delegue` (0 = normal, 1 = délégué, 2 = suppléant)
- `floutage` (booléen)

Exemple de sortie :
```python
[
    {"id": "1", "prenom": "Alice", "nom": "Martin", "delegue": 1, "floutage": False},
    {"id": "2", "prenom": "Bob", "nom": "Durand", "delegue": 0, "floutage": True},
]
```

---

###  `fonction_img.py`
Ce module regroupe toutes les opérations sur les images, en utilisant la librairie Pillow.

#### Fonctions principales :

1. `redimensionner_image(image, largeur, hauteur)`
   - Redimensionne une image selon la méthode du plus proche voisin.
   - C’est une méthode simple : chaque pixel de l’image redimensionnée prend la valeur du pixel le plus proche dans l’image originale.
   - Implémentée avec :
     ```python
     image.resize((largeur, hauteur), resample=Image.NEAREST)
     ```

2. `noir_et_blanc(image)`
   - Convertit une image couleur en niveaux de gris avec :
     ```python
     ImageOps.grayscale(image)
     ```

3. `flouter_image(image, rayon=3)`**
   - Applique un flou uniforme sur l’image à l’aide d’un Box Blur standard de Pillow :
     ```python
     image.filter(ImageFilter.BoxBlur(rayon))
     ```
   - Chaque pixel devient la moyenne des pixels voisins dans une zone carrée de rayon défini.

4. `ajouter_badge(image, delegue)`
   - Ajoute un petit cercle coloré dans le coin supérieur droit de la photo :
     - Bleu = délégué (`delegue == 1`)
     - Orange = suppléant (`delegue == 2`)
   - Aucun badge pour les autres étudiants.
   - Implémente via `ImageDraw.Draw` et `draw.ellipse()`.

---

###  `fonction_pdf.py`
C’est le module central de génération du yearbook.  
Il crée successivement :
1. Une page de garde
2. Une page photo de classe
3. Plusieurs pages étudiants

#### Fonctions principales :

| Fonction | Rôle |
|-----------|------|
| `creer_page_garde(logo_path, titre, taille)` | Crée la page de garde avec le logo et le titre |
| `creer_page_photo_classe(photo_path, taille)` | Affiche la photo de groupe de la promotion |
| `creer_pages_etudiants(...)` | Génère les pages individuelles avec les photos, noms, citations, etc. |
| `creer_yearbook_pdf(...)` | Assemble toutes les pages et exporte le fichier PDF final |

---

##  3. Fonctionnement des algorithmes

###  3.1 Redimensionnement (Plus proche voisin)
Le principe du plus proche voisin :
- Pour chaque pixel de la nouvelle image, on cherche le pixel le plus proche dans l’image originale.
- Avantage : rapide, conserve les bords nets.
- Inconvénient : pixelisation visible si on agrandit beaucoup.

Formule simplifiée :
```
nouveau_pixel(x, y) = original_pixel(round(x * ratio_x), round(y * ratio_y))
```

---

###  3.2 Floutage (Box Blur)
Le Box Blur consiste à remplacer chaque pixel par la moyenne des pixels voisins dans une zone carrée de rayon `r`.

Exemple :
```
rayon = 1 → moyenne des 9 pixels voisins
rayon = 2 → moyenne des 25 pixels voisins
```

Dans Pillow, cela se fait avec :
```python
image.filter(ImageFilter.BoxBlur(rayon))
```

---

##  4. Commandes clés de la librairie Pillow utilisées

| Commande | Rôle |
|-----------|------|
| `Image.open(path)` | Ouvre une image |
| `image.convert("RGB")` | Convertit en mode couleur standard |
| `image.resize((w, h), resample=Image.NEAREST)` | Redimensionne une image |
| `ImageOps.grayscale(image)` | Transforme une image en noir et blanc |
| `image.filter(ImageFilter.BoxBlur(r))` | Applique un flou |
| `ImageDraw.Draw(image)` | Permet de dessiner sur une image |
| `draw.text((x, y), texte, font=font, fill=couleur)` | Écrit du texte |
| `draw.ellipse((x1, y1, x2, y2), fill=couleur)` | Dessine un cercle ou ovale |
| `image.paste(img, position, mask)` | Colle une image sur une autre (avec transparence) |
| `image.save("fichier.pdf", save_all=True, append_images=[...])` | Exporte le yearbook complet en PDF |

---

##  5. Options globales supportées

- Format : paysage ou portrait  
- Mode photo : couleur ou noir et blanc  
- Affichage citations : avec ou sans  
- Badges délégué/suppléant 
- Floutage sélectif(selon le CSV)  
- Sortie finale: fichier PDF en format A4 (`output/yearbook.pdf`)

---

##  6. Conclusion

Ce projet met en œuvre :
- Une bonne structuration en modules (lisibilité, modularité).
- Une utilisation propre de la librairie Pillow pour la manipulation d’images.
- Des algorithmes implémentés à la main pour le redimensionnement et le floutage.
- Des options de personnalisation globales respectant le cahier des charges.

Le résultat final est un yearbook PDF complet, automatique et personnalisable.
