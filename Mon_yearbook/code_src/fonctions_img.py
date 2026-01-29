from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont


def redimensionner_image(image, largeur, hauteur):
    """Redimensionne une image avec un algorithme simple."""
    src = image.convert("RGB")
    dst = Image.new("RGB", (largeur, hauteur))
    w0, h0 = src.size
    for y in range(hauteur):
        for x in range(largeur):
            xs = int(x * w0 / largeur)
            ys = int(y * h0 / hauteur)
            dst.putpixel((x, y), src.getpixel((xs, ys)))

    return dst


def noir_et_blanc(image):
    """Convertit une image en noir et blanc."""
    return ImageOps.grayscale(image)


def flouter_image(image, rayon=3):
    """Applique un flou (box blur) avec pillow."""
    return image.filter(ImageFilter.BoxBlur(rayon))


def ajouter_badge(image, delegue):
    """Ajoute un badge si l’étudiant est délégué ou suppléant. """
    try:
        delegue = int(delegue)
    except Exception:
        delegue = 0

    if delegue == 0:
        return image


    bw = max(40, int(min(image.width, image.height) * 0.22))
    bh = bw
    badge = Image.new("RGBA", (bw, bh), (255, 255, 255, 0))
    draw = ImageDraw.Draw(badge)

    # couleur
    if delegue == 1:
        couleur = (0, 100, 255, 230)  # Bleu délégué
        texte = "D"
    elif delegue == 2:
        couleur = (255, 150, 0, 230)  # Orange suppléant
        texte = "S"
    else:
        return image

    # Dessine le badge (cercle plein)
    draw.ellipse((0, 0, bw - 1, bh - 1), fill=couleur)


    try:
        font = ImageFont.truetype("arial.ttf", int(bw * 0.6))
    except Exception:
        font = ImageFont.load_default()

    
    tw = th = None
    try:
        if hasattr(font, 'getsize'):
            tw, th = font.getsize(texte)
    except Exception:
        tw = th = None

    if tw is None or th is None:
        try:
            tmp = Image.new('RGBA', (1, 1))
            tmpdraw = ImageDraw.Draw(tmp)
            if hasattr(tmpdraw, 'textbbox'):
                tb = tmpdraw.textbbox((0, 0), texte, font=font)
                tw = tb[2] - tb[0]
                th = tb[3] - tb[1]
        except Exception:
            tw = th = None

    if tw is None or th is None:
        try:
            mask = font.getmask(texte)
            tw, th = mask.size
        except Exception:
            tw = th = None

    if tw is None or th is None:
    
        size = getattr(font, 'size', None)
        if size:
            tw = int(len(texte) * size * 0.6)
            th = int(size)
        else:
            tw = len(texte) * 6
            th = int(bh * 0.6)

    
    draw.text(((bw - tw) / 2, (bh - th) / 2), texte, fill="white", font=font)


    margin = max(6, int(bw * 0.12))
    paste_x = max(0, image.width - bw - margin)
    paste_y = margin
    try:
        image.paste(badge, (paste_x, paste_y), badge)
    except Exception:

        image = image.convert('RGBA')
        image.alpha_composite(badge, (paste_x, paste_y))

    return image