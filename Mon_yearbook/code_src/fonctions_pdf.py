from PIL import Image, ImageDraw, ImageFont
from fonctions_img import noir_et_blanc, flouter_image, ajouter_badge
import math
from pathlib import Path


def _load_font(name, size):
    """Charge une police, ou la police par défaut si absente."""
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


def creer_page_garde(logo_path, titre, taille):
    """Crée la page de garde avec le logo et le titre du yearbook."""
    page = Image.new("RGB", taille, "white")
    draw = ImageDraw.Draw(page)

    logo_path = Path(logo_path)
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA").resize((500, 500))
        page.paste(logo, (int(taille[0]/2 - 250), 400), logo)

    font = _load_font("arial.ttf", 80)  # Arial si dispo
    draw.text((taille[0]/2, 1000), titre, fill="black", font=font, anchor="mm")
    return page


def creer_page_photo_classe(photo_classe_path, taille):
    """Crée la page avec la photo de classe."""
    page = Image.new("RGB", taille, "white")
    draw = ImageDraw.Draw(page)
    font = _load_font("arial.ttf", 70)
    draw.text((taille[0]/2, 200), "Photo de classe", fill="black", font=font, anchor="mm")

    photo_classe_path = Path(photo_classe_path)
    
    if not photo_classe_path.exists():
        alt_data = Path('data') / 'photoClasse.png'
        alt_res = Path('ressources') / 'photo_classe.png'
        if alt_data.exists():
            photo_classe_path = alt_data
        elif alt_res.exists():
            photo_classe_path = alt_res

    if photo_classe_path.exists():
        try:
            photo = Image.open(photo_classe_path).convert("RGB")
            photo.thumbnail((2000, 2500))
            x = (taille[0] - photo.width) // 2
            y = (taille[1] - photo.height) // 2 + 200
            page.paste(photo, (x, y))
        except Exception:
            # si l'image est corrompue ou illisible, on laisse la page blanche
            pass
    return page


def creer_pages_etudiants(etudiants, dossier_photos, dossier_citations,
                          avec_citations=True, format_paysage=True, noir_blanc=False):
    """Crée toutes les pages des étudiants selon les options choisies."""
    pages = []

    # Format
    if format_paysage:
        taille = (3508, 2480)
        nb_lignes, nb_par_ligne = (2, 5) if avec_citations else (3, 5)
    else:
        taille = (2480, 3508)
        nb_lignes, nb_par_ligne = (3, 3) if avec_citations else (5, 3)

    largeur_case = taille[0] // nb_par_ligne
    hauteur_case = (taille[1] - 300) // nb_lignes
    font_nom = _load_font("arial.ttf", 40)
    font_cit = _load_font("ariali.ttf", 30)
    nb_par_page = nb_par_ligne * nb_lignes

    def _wrap_text(text, font, max_width, draw):
        """Retourne une citation coupée sur plusieurs lignes."""
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = cur + " " + w if cur else w
            if draw.textlength(test, font=font) <= max_width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    for page_num in range(math.ceil(len(etudiants) / nb_par_page)):
        page = Image.new("RGB", taille, "white")
        draw = ImageDraw.Draw(page)
        draw.text((taille[0]/2, 100), "Étudiants de la promotion", fill="black", font=font_nom, anchor="mm")

        for i in range(nb_par_page):
            index = page_num * nb_par_page + i
            if index >= len(etudiants):
                break

            etu = etudiants[index]
            col, ligne = i % nb_par_ligne, i // nb_par_ligne
            x = col * largeur_case + 50
            y = 200 + ligne * hauteur_case

            # Chargement de la photo
            photo_path = Path(dossier_photos) / f"{etu['id']}.jpg"
            if not photo_path.exists():
                photo_path = Path(dossier_photos) / f"{etu['id']}.jpeg"

            if not photo_path.exists():
                draw.rectangle([x, y, x + (largeur_case - 100), y + (hauteur_case - 150)], outline="black")
            else:
                try:
                    image = Image.open(photo_path).convert("RGB")

                    # Application des effets noir et blanc et floutage
                    if noir_blanc:
                        image = noir_et_blanc(image)
                    if etu.get("floutage"):
                        image = flouter_image(image, rayon=5)
                    image.thumbnail((largeur_case - 100, hauteur_case - 140))
                    image = ajouter_badge(image, etu.get("delegue", 0))
                    img_x = x + ((largeur_case - 100 - image.width) // 2)
                    img_y = y + ((hauteur_case - 140 - image.height) // 2)
                    page.paste(image, (img_x, img_y))
                except Exception:
                    draw.rectangle([x, y, x + (largeur_case - 100), y + (hauteur_case - 150)], outline="black")

            # Nom complet et ID
            name_y = y + (hauteur_case - 120)
            draw.text((x + (largeur_case - 100)/2, name_y),
                      f"{etu.get('prenom','')} {etu.get('nom','')}", fill="black", font=font_nom, anchor="mm")
            # Dessiner l'ID en haut à gauche
        id_text = etu.get('id', '')
        if id_text:
            id_font = _load_font("arial.ttf", 18)
            draw.text((x + 8, y + 8), id_text, fill="black", font=id_font)

            # Citation
            if avec_citations:
                citation_path = Path(dossier_citations) / f"{etu['id']}.txt"
                if citation_path.exists():
                    citation = citation_path.read_text(encoding="utf-8").strip()
                    lines = _wrap_text(citation, font_cit, largeur_case - 120, draw)
                    for j, line in enumerate(lines[:3]):
                        draw.text((x + (largeur_case - 100)/2, name_y + 50 + j*35),
                                  line, fill="gray", font=font_cit, anchor="mm")

        print(f"Page {page_num + 1} générée avec succès.")
        pages.append(page)

    return pages


def creer_yearbook_pdf(logo_path, photo_classe_path, etudiants,
                       dossier_photos, dossier_citations, titre,
                       sortie_pdf, avec_citation=False, format_paysage=True, noir_blanc=False):
    """Assemble le yearbook complet et le sauvegarde en PDF."""
    sortie_pdf = Path(sortie_pdf)
    sortie_pdf.parent.mkdir(parents=True, exist_ok=True)

    taille = (3508, 2480) if format_paysage else (2480, 3508)

    pages = [
        creer_page_garde(logo_path, titre, taille),
        creer_page_photo_classe(photo_classe_path, taille)
    ]

    pages.extend(creer_pages_etudiants(
        etudiants, dossier_photos, dossier_citations,
        avec_citations=avec_citation, format_paysage=format_paysage, noir_blanc=noir_blanc
    ))

    pages[0].save(str(sortie_pdf), save_all=True, append_images=pages[1:])
    print("✅ Yearbook créé avec succès :", sortie_pdf)
