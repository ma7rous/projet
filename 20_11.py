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
    Renvoie cette matrice M et la valeur maximal que prend M[i,j] nbr_tag.
    M[i,j]=0 correspond à un pixel blanc et M[i,j]!=0 correspond à un pixel noir.
    Si deux éléments de M ont une même valeur non nul, alors ils appartiennent au même caractère (la réciproque est fausse à la fin de cette fonction).
    
    Argument: image--> une image, en noir et blanc, lue par le biais de la bibliothèque PIL.
    '''
    colonne,ligne = image.size
    M=np.zeros((ligne, colonne), dtype=np.uint8)
    nbr_tag=0
    for i in range(ligne):
        for j in range(colonne):
            if img.getpixel((j,i))[0] < 100:
                if M[i,j-1]!=0: M[i,j]=M[i,j-1]
                elif M[i-1,j-1]!=0: M[i,j]=M[i-1,j-1]
                elif M[i-1,j]!=0: M[i,j]=M[i-1,j]
                else:
                    nbr_tag+=1
                    M[i,j]=int(nbr_tag)
    return M, nbr_tag

def ebaucheMemeTag(M):
    '''Renvoie une liste pair_liste de sous-listes à deux éléments correspondant à deux tags voisins de la matrice tagué M.
    
    Argument: M--> matrice contenant des entiers (un élément nul correspond à un pixel blanc).
    '''
    ligne, colonne = np.shape(M)
    pair_liste=[]
    for i in range(1, ligne-1):
        for j in range(1,colonne-1):
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



def memeTag(pair_liste, nbr_tag):
    '''Renvoie une liste tag_liste de sous-listes. Chaque sous liste contient les tags correspondant à un même caractère de la matrice recherchée.
    
    Arguments:
        -pair_liste: liste de sous-listes à deux éléments construite et renvoyé par ebaucheMemeTag ;
        -nrb_tag: un entier correspondant à la valeur maximal que peut prendre un élément de la matrice.
    '''
    tag_liste=[]
    solo_tag = [[i+1] for i in range(nbr_tag)]
    if len(pair_liste)!=0:
        couple = pair_liste.pop(0)
        tag_liste.append(couple)
        solo_tag.remove(couple[0]), solo_tag.remove(couple[1])
        while len(pair_liste)!=0:
            couple = pair_liste.pop(0)
            if couple[0] in solo_tag: solo_tag.remove(couple[0])
            if couple[1] in solo_tag: solo_tag.remove(couple[1])
            
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
    tag_liste += solo_tag
    return tag_liste

def matriceTague(M, tag_liste):
    ligne, colonne = np.shape(M)
    n=len(tag_liste)
    position_caracteres = [[ligne, -1, colonne, -1] for i in range(n)]
    position_caracteres = np.array(position_caracteres)
    #liste de la forme [[i1_min, i1_max, j1_min, j1_max], ..., [in_min, in_max, jn_min, jn_max]] avec 1,...,n les différennts caractères
    nombre_pixels = [0]*n
    for i in range(ligne):
        for j in range(colonne):
            if M[i,j]!=0:
                for k in range(n):
                    if M[i,j] in tag_liste[k]:
                        M[i,j] = k+1
                        nombre_pixels[k] += 1
                        if i<position_caracteres[k, 0]: position_caracteres[k, 0] = i
                        elif i>position_caracteres[k, 1]: position_caracteres[k, 1] = i
                        if j<position_caracteres[k, 2]: position_caracteres[k, 2] = j
                        elif j>position_caracteres[k, 3]: position_caracteres[k, 3] = j
                        break
    return position_caracteres, nombre_pixels


def sauvergarder_regions(image, M, position_caracteres, nom_position='regions.txt', nom_image="Charactère_", format='.jpg'):
    fichier=open(nom_position,'w')
    for k in range(len(position_caracteres)):
        imin, jmin = position_caracteres[k][0], position_caracteres[k][2]
        img = image.crop((jmin-1, imin-1, position_caracteres[k][3]+1, position_caracteres[k][1]+1))
        img.save(nom_image+str(k+1)+format)
        img.show()
        string = str(imin)+'; '+ str(jmin)
        fichier.write(string+'\n')
    fichier.close()

def afficheListeTag(image):
    M, nbr_tag = convMatrice(image)
    pair_liste = ebaucheMemeTag(M)
    tag_liste = memeTag(pair_liste, nbr_tag)
    print(tag_liste)
    position_caracteres, nombre_pixels = matriceTague(M, tag_liste)
    print(position_caracteres, nombre_pixels)
#    Matr=np.zeros((ligne, colonne), dtype=np.uint8)
#    for i in range(ligne):
#        for j in range(colonne):
#            if M[i,j]==3:
#                Matr[i,j]=1
#    Matr=Matr*255
#    a=Image.fromarray(Matr)
#    a.show()
    sauvergarder_regions(img, M, position_caracteres)

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
img = Image.open('test2.png') # The image file must exist in the same directory as the script

afficheListeTag(img) 
#Image.fromarray()
#img.save('')
#img.show()
                  
