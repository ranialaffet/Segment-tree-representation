import sys,pygame
import traceback
from PIL import Image
from colormath.color_objects import sRGBColor
time=0

class Context:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            setattr(self, key, val)


def test_callback(do_something,tableau, n, debut_somme, fin_somme, nom_fichier,init=None):
    pygame.init()
    clock = pygame.time.Clock()
    window_size = width, height = 700, 500
    screen = pygame.display.set_mode(window_size)
    time_game=0
    KEEPGOING=True
    context=Context({
        'screen':screen,
        'background': sRGBColor(1,1,1),
        'foreground': sRGBColor(0,0,0),
        'width': width,
        'height': height,
        'font': pygame.font.Font(None, 16)
    })
    while KEEPGOING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                KEEPGOING=False
        if not KEEPGOING:
            continue
        # Clear the screen
        time_game += clock.tick(60) / 1000.0
        try:
            do_something(context,time_game, tableau, n, debut_somme, fin_somme, nom_fichier)
            # Update the display
            pygame.display.flip()
        except Exception as e:
            print("Error")
            traceback.print_exc()
            pygame.quit()
            KEEPGOING=False
    print("Window closed")

def SurfaceTopilImage(surface,transparent=False):
    mode="RGBA" if transparent else "RGB"
    pil_string_image = pygame.image.tostring(surface,mode,False)
    return Image.frombytes(mode,surface.get_size(),pil_string_image)


import math
import pygame
from colormath.color_objects import sRGBColor
from collections import OrderedDict

def effacer_ecran(screen, background):
    """Efface l'écran en remplissant avec une couleur de fond."""
    screen.fill(background.get_upscaled_value_tuple())

def verifier_puissance_de_2(tableau):
    """Vérifie que la longueur du tableau est une puissance de 2."""
    n = len(tableau)
    assert math.log2(n).is_integer(), "La longueur du tableau doit être une puissance de 2"
    return n, int(math.log2(n))

def calculer_positions(tableau, largeur, hauteur, marge, somme_section):
    """Calcule les positions des nœuds dans l'arbre de segments."""
    n, k = verifier_puissance_de_2(tableau)
    largeur_rect = (largeur - 2 * marge) / (2 * n-1)
    hauteur_rect = min((hauteur - 2 * marge - somme_section) / (3 * k +2), largeur_rect)
    noeuds = OrderedDict()

    row = k
    nb_by_row = n
    y_rect = marge + hauteur_rect * 3 * row
    x_rect = marge
    skip_between = 2

    # Dernière ligne
    for i in range(n):
        id_noeud = i + nb_by_row
        valeur = tableau[i]
        noeuds[id_noeud] = {'id': id_noeud, 'x': x_rect, 'y': y_rect, 'valeur': valeur}
        x_rect += skip_between * largeur_rect

    # Autres lignes
    while row > 0:
        row -= 1
        y_rect = marge + hauteur_rect * 3 * row
        skip_before = skip_between - 1
        x_rect = marge + skip_before * largeur_rect
        skip_between *= 2
        nb_by_row //= 2

        for i in range(nb_by_row):
            id_noeud = i + nb_by_row
            valeur = noeuds[id_noeud * 2]['valeur'] + noeuds[id_noeud * 2 + 1]['valeur']
            noeuds[id_noeud] = {'x': x_rect, 'y': y_rect, 'valeur': valeur}
            x_rect += skip_between * largeur_rect

    return noeuds, largeur_rect, hauteur_rect

def dessiner_legend(screen, font, foreground):
    """Dessine la légende de l'arbre."""
    pygame.draw.rect(screen, (173, 216, 230), (5, 5, 25, 25))
    pygame.draw.rect(screen, (0, 0, 0), (5, 5, 25, 25), 2)
    texte = font.render('Contient la somme des nœuds  enfants', True, foreground.get_upscaled_value_tuple())
    screen.blit(texte, (35, 10))

def dessiner_titre(screen, font, foreground, largeur, hauteur, marge):
    """Dessine le titre."""

    texte = font.render("Segment Tree dans les requêtes d'intervalles", True, foreground.get_upscaled_value_tuple())
    screen.blit(texte, (largeur//2-150, hauteur-marge//2))


def dessiner_noeuds_et_lignes(screen, noeuds, largeur_rect, hauteur_rect, font, foreground, noeuds_a_afficher):
    """Dessine les nœuds et les lignes parent-enfant."""
    compteur = 0
    for id_noeud, noeud in noeuds.items():
        if compteur >= noeuds_a_afficher:
            break
        compteur += 1

        if id_noeud <= len(noeuds) // 2:
            parent = noeud
            enfant_gauche = noeuds[id_noeud * 2]
            enfant_droit = noeuds[id_noeud * 2 + 1]
            x1, y1 = parent['x'] + largeur_rect / 2, parent['y'] + hauteur_rect
            x2_gauche, y2_gauche = enfant_gauche['x'] + largeur_rect / 2, enfant_gauche['y']
            x2_droit, y2_droit = enfant_droit['x'] + largeur_rect / 2, enfant_droit['y']

            pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2_gauche, y2_gauche), 2)
            pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2_droit, y2_droit), 2)
            pygame.draw.rect(screen, (173, 216, 230), (noeud['x'], noeud['y'], largeur_rect, hauteur_rect))

        pygame.draw.rect(screen, (0, 0, 0), (noeud['x'], noeud['y'], largeur_rect, hauteur_rect), 2)
        texte = font.render(str(noeud['valeur']), True, foreground.get_upscaled_value_tuple())
        texte_rect = texte.get_rect(center=(noeud['x'] + largeur_rect / 2, noeud['y'] + hauteur_rect / 2))
        screen.blit(texte, texte_rect)

        # Afficher l'indice du noeud
        texte = font.render(str(id_noeud), True, foreground.get_upscaled_value_tuple())
        texte_rect = texte.get_rect(center=(noeud['x'] + largeur_rect / 2, noeud['y'] + 3*hauteur_rect / 2))
        screen.blit(texte, texte_rect)

def afficher_somme(context, noeuds, marge, hauteur, somme_section, debut_somme, fin_somme):
    """Affiche les informations sur la somme d'une plage donnée."""
    font = context.font
    screen = context.screen
    foreground = context.foreground
    n = len(noeuds) // 2
    l, r = n + debut_somme, fin_somme + n
    y_text = hauteur - somme_section - marge
    text_somme = f"Pour avoir la somme à partir de ({debut_somme}-{fin_somme}) dans la liste qui correnspondent à ({l}-{r}) dans l'arbre, on prend :"
    texte = font.render(text_somme, True, foreground.get_upscaled_value_tuple())
    screen.blit(texte, (marge, y_text))
    y_text += 15

    r+=1
    ra, rb = 0, 0
    while l < r:
        if l & 1:
            ra += noeuds[l]['valeur']
            texte = font.render(f"- Le nœud {l} ayant la valeur : {noeuds[l]['valeur']}", True, foreground.get_upscaled_value_tuple())
            screen.blit(texte, (marge + 10, y_text))
            y_text += 15
            l += 1

        if r & 1:
            r -= 1
            rb += noeuds[r]['valeur']
            texte = font.render(f"- Le nœud {r} ayant la valeur : {noeuds[r]['valeur']}", True, foreground.get_upscaled_value_tuple())
            screen.blit(texte, (marge + 10, y_text))
            y_text += 15

        l //= 2
        r //= 2

    texte = font.render(f"La somme finale est : {ra + rb}", True, foreground.get_upscaled_value_tuple())
    screen.blit(texte, (marge, y_text))

def dessiner_segment_tree(context,temps, tableau, n, debut_somme, fin_somme, nom_fichier):
    """Dessine un arbre de segments progressivement."""
    screen = context.screen
    largeur, hauteur = context.width, context.height
    marge = 50
    somme_section = 80

    effacer_ecran(screen, context.background)

    noeuds, largeur_rect, hauteur_rect = calculer_positions(tableau, largeur, hauteur, marge, somme_section)
    dessiner_legend(screen, context.font, context.foreground)
    dessiner_titre(screen, context.font, context.foreground, largeur, hauteur, marge)

    noeuds_a_afficher = int(temps * 5)
    dessiner_noeuds_et_lignes(screen, noeuds, largeur_rect, hauteur_rect, context.font, context.foreground, noeuds_a_afficher)
    afficher_somme(context, noeuds, marge, hauteur, somme_section, debut_somme, fin_somme)
    ximg=SurfaceTopilImage(screen)
    ximg.save(f"{nom_fichier}.png")
    


if __name__ == "__main__":
    tableau=[]
    n = int(input("donner la taille du tableau : "))
    for i in range(n):
        x= int(input("donner le nombre "+ str(i+1)+": "))
        tableau.append(x)
        
    debut_somme = int(input("donner la position du debut de la somme que vous voullez effectué (1-"+str(n)+") : "))
    while debut_somme < 1 or debut_somme > n:
        debut_somme = int(input("donner la position du debut de la somme que vous voullez effectué (1-"+str(n)+") : "))

    fin_somme = int(input("donner la position de la fin de la somme que vous voullez effectué ("+str(debut_somme)+"-"+str(n)+") : "))
    while fin_somme < 1 or fin_somme > n or fin_somme < debut_somme:
        fin_somme = int(input("donner la position de la fin de la somme que vous voullez effectué ("+str(debut_somme)+"-"+str(n)+") : "))

    nom_fichier = input("donner le nom avec lequel le resultat va être sauvegarder: ")
    
    # Rendre la taille du tableau en puissance de 2 
    nn = 2 ** math.ceil(math.log2(n))
    tableau.extend([0] * (nn - n))
    
    test_callback(dessiner_segment_tree, tableau, n, debut_somme, fin_somme, nom_fichier)

