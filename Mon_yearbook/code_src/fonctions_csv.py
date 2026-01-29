import csv

def lire_csv(fichier_csv:str) -> list[dict]:
    
    """Lit le fichier CSV des etudiants  et renvoie la liste
      sous forme de dictionnaires avec les champs: id, prenom,
      nom, delegue, floutage."""

    etudiants = []

    with open(fichier_csv, newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f, delimiter=',')

        for ligne in lecteur:
            #recuperation de l'id etudiant
            id_val= ligne.get('id', '').strip()
            if not id_val:
                # si l'id est manquant, on ignore cette ligne
                continue

            #recuperation du nom et prenom etudiant
            prenom= ligne.get('prenom', '').strip()
            nom= ligne.get('nom', '').strip()

            #recuperation du statut delegue(0,1,2)
            val_delegue= ligne.get('delegue', '0').strip().lower()
            try:
                delegue= int(val_delegue)
            except:
                delegue=0   # on considere membre normal, si il y a une erreur

            # verification du statut floutage 
            flou_str= ligne.get('floutage', '').strip().lower()
            floutage= flou_str == 'true'

            # ajout de l'etudiant a la liste
            etudiants.append({
                'id': id_val,
                'prenom': prenom,
                'nom': nom,
                'delegue': delegue,
                'floutage': floutage
            })

    return etudiants