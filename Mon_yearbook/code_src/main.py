import os
from pathlib import Path
from fonctions_csv import lire_csv as lire_etudiants
from fonctions_pdf import creer_yearbook_pdf

def main():
    #dossier principaux
    dossier_data=Path("data")
    dossier_sortie=Path("output")
    dossier_ressources=Path("ressources")

    if not dossier_sortie.exists():
     os.makedirs(dossier_sortie)
     print("Dossier de sortie 'output' cree.")

    #fichier csv des etudiants
    print ("Lecture du fichier CSV des etudiants...")
    fichier_csv= dossier_data / "etudiants.csv"
    etudiants= lire_etudiants(fichier_csv)
    print (f"{len(etudiants)} etudiants trouves dans le fichier CSV.")

    # Options du yearbook (a personnaliser selon besoins)
    avec_citations= True    # false pour ne pas afficher les citations
    format_paysage= True    # false pour portrait
    noir_et_blanc= False    # true pour photos en noir et blanc

    # creation du yearbook
    print("Creation du yearbook PDF en cours...")
    creer_yearbook_pdf(
        logo_path=dossier_ressources / "SUPINFO_LOGO_QUADRI.png",
        photo_classe_path=dossier_data / "photo_classe.png",
        etudiants=etudiants,
        dossier_photos=dossier_data / "images",
        dossier_citations=dossier_data / "citations",
        titre="BSc1 - SUPINFO Paris - 2025-2026",
        sortie_pdf=dossier_sortie / "yearbook.pdf",
        avec_citation=avec_citations,
        format_paysage=format_paysage,
        noir_blanc=noir_et_blanc
    )

    print ("✅ Yearbook généré avec succès dans le dossier_sortie 'output' ! ")

main() 