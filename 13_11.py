# -*- coding: utf-8 -*-

#################################################
#                 Bibliothèques                 #
#################################################
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

#################################################
#                   Fonctions                   #
#################################################

def convMatrice(image):
    '''Convertie une image en noir et blanc en une matrice M.
    M[i,j]=0 correspond à un pixel blanc et M[i,j]!=0 correspond à un pixel noir.
    Si deux éléments de M ont une même valeur non nul, alors ils appartiennent au même caractère (la réciproque est fausse à la fin de cette fonction).
    
    Argument: image--> une image, en noir et blanc, lue par le biais de la bibliothèque PIL.
    '''
    global largeur, hauteur
    hauteur, largeur = image.size
    M=np.zeros((largeur, hauteur), dtype=np.uint8)
    nbr_charactere=0
    for i in range(largeur):
        for j in range(hauteur):
            if img.getpixel((j,i))[0] < 100:
                if M[i,j-1]!=0: M[i,j]=M[i,j-1]
                elif M[i-1,j-1]!=0: M[i,j]=M[i-1,j-1]
                elif M[i-1,j]!=0: M[i,j]=M[i-1,j]
                else:
                    nbr_charactere+=1
                    M[i,j]=int(nbr_charactere)
    return M

def ebaucheSametag(M):
    '''Créer une première ébauche d'une liste (pair_liste) qui contiendra des listes dont chacunes d'entre elles contiendra tout les tags correspondant à un même caractère.
    
    Argument: M--> matrice contenant des entiers (un élément nul correspond à un pixel blanc).
    '''
    pair_liste=[]
    for i in range(1, largeur-1):
        for j in range(1,hauteur-1):
            if M[i,j]!=0:
                tag=M[i,j]
                voisins=[ M[i,j-1], M[i-1,j-1], M[i-1,j] ]
                
                if voisins[0]!=0 and voisins[0]!=tag and [ min( tag, voisins[0] ), max( tag, voisins[0] )] not in pair_liste:
                    pair_liste.append( [min( tag, voisins[0] ), max( tag, voisins[0] )] )
                
                elif voisins[1]!=0 and voisins[1]!=tag and [ min( tag, voisins[1] ), max( tag, voisins[1] )] not in pair_liste:
                    pair_liste.append( [min( tag, voisins[1] ), max( tag, voisins[1] )] )
                
                elif voisins[2]!=0 and voisins[2]!=tag and [ min( tag, voisins[2] ), max( tag, voisins[2] )] not in pair_liste:
                    pair_liste.append( [min( tag, voisins[2] ), max( tag, voisins[2] )] )
                
    return pair_liste
#
#def rechercheDansListe(tag, TAGS, pair_liste, k=0):
#    '''Fonction récursive qui modifie la liste TAGS et la liste pair_liste.
#    Cherche les sous listes (de taille 2) de pair_liste à partir de l'indice k, ayant tag pour une de ces deux valeurs, afin d'ajouter la deuxième valeur dans la liste TAGS.
#    Le couple est ensuite supprimé de la liste pair_liste.
#    
#    Arguments:
#        tag: entier (correspond à un tag);
#        TAGS: liste (correspond à la sous liste de tag_liste);
#        pair_liste: liste de listes de taille 2 contenant des entiers (des tags);
#        k: entier, nul par défaut (correspond à l'indice de départ pour la recherche dans pair_liste).
#    '''
#    for i in range(k, len(pair_liste)):
#        indice=i
#        x=pair_liste[indice]
#        if tag in x:            
#            if x[1] not in TAGS:
#                TAGS.append(x[1])
#            else:
#                TAGS.append(x[0])
#            pair_liste.pop(i)
#            #len(pair_liste) est modifié, on sort de la boucle pour rappeler la fonction f avec "indice" comme initialisation de la nouvelle boucle
#            break
#    if indice>=len(pair_liste)-1: #on est pas rentré dans le "if tag in x", donc on a exploré la liste pair_liste en entier
#        return 
#    rechercheDansListe(tag, TAGS, pair_liste, indice)
#
#def sameTag(tag_liste, pair_liste):
#    '''Fonction récursive qui utilise la fonction rechercheDansListe, et qui modifie les listes tag_liste et pair_liste.
#    Permet de créer une liste (tag_liste) de liste contenant les tags correspondant aux mêmes caractères.
#
#    Arguments:
#        tag_liste: liste (l'utilisateur doit rentrer une liste vide);
#        pair_liste: liste de listes de taille 2 contenant des entiers (des tags).
#    '''
#    TAGS=pair_liste.pop(0)
#    tag_liste.append(TAGS)
#    for i in TAGS:
#        if len(pair_liste)==0:
#            return
#        #on cherche les couples ayant un membre égale à i dans la liste pair_liste, et on l'ajoute dans TAGS
#        rechercheDansListe(i ,TAGS, pair_liste)
#    if len(pair_liste)!=0:  #TAGS n'est pas le dernier caractère, il en reste d'autres
#        sameTag(tag_liste, pair_liste)



def MemeTag(pair_liste):
    tag_liste=[]
    tag_liste.append(pair_liste.pop(0))
    while len(pair_liste)!=0:
        couple=pair_liste.pop(0)
        i0, i1 = None, None
        for i in range(len(tag_liste)):
            tags=list(tag_liste[i])
            if i0 is None and couple[0] in tags: i0=i
            if i1 is None and couple[1] in tags: i1=i                  
        if i0 is None:
            if i1 is None: tag_liste.append(couple)
                # aucun des arguments du couple est présent dans une des sous listes de tag_liste.
            else: tag_liste[i1].append(couple[0])
                # couple[1] appartient à la i1 ème sous liste de tags mais i0 n'est pas dans tag_liste.
        elif i1 is None: tag_liste[i0].append(couple[1])
            # couple[0] appartient à la i0 ème sous liste de tags mais i1 n'est pas dans tag_liste.     
        else:
            # couple[0] et couple[1] sont respectivement dans la i0 ème et i1 ème sous liste de tag_liste.
            if i0!=i1:
                imin = min(i0,i1)
                tags=tag_liste.pop(max(i0,i1))
                for k in tags:
                    tag_liste[imin].append(k)
    return tag_liste

def matriceTague(M, tag_liste):
    n=len(tag_liste)
    position_caracteres=[[largeur,-1,hauteur,-1] for i in range(n)]
    #liste de la forme [[i1_min, i1_max, j1_min, j1_max], ..., [in_min, in_max, jn_min, jn_max]] avec 1,...,n les différennts caractères
    nombre_pixels=[0]*n
    for i in range(largeur):
        for j in range(hauteur):
            if M[i,j]!=0:
                for k in range(n):
                    if M[i,j] in tag_liste[k]:
                        M[i,j]=k+1
                        nombre_pixels[k]+=1
                        if i<position_caracteres[k][0]: position_caracteres[k][0] = i
                        elif i>position_caracteres[k][1]: position_caracteres[k][1] = i
                        if j<position_caracteres[k][2]: position_caracteres[k][2] = j
                        elif j>position_caracteres[k][3]: position_caracteres[k][3] = j
                        break
    return position_caracteres, nombre_pixels
        
def afficheListeTag(image):
    M = convMatrice(image)
    pair_liste = ebaucheSametag(M)
    tag_liste = MemeTag(pair_liste)
    position_caracteres, nombre_pixels = matriceTague(M, tag_liste)
    print(position_caracteres, nombre_pixels)
    M=M*255#/len(nombre_pixels)
    a=Image.fromarray(M)
    a.show()

#def afficheListeTag_bis(image):
#    M=convMatrice(image)
#    tag_liste=[]
#    sameTag(tag_liste, ebaucheSametag(M))
#    tag_liste[0].sort()
#    print(tag_liste)

##################################################
#                   Variables                    #
##################################################

##################################################
#                     Main                       #
##################################################
img = Image.open('Capture3.png') # The image file must exist in the same directory as the script
img=img.convert('LA')

afficheListeTag(img) 




                  

       
               