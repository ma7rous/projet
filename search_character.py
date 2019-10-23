# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#################################################
#                 Bibliothèques                 #
#################################################
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

#################################################
#                   Fonctions                   #
#################################################

def Recherche_noir_cadre(x,y):
    min_y=y
    max_y=y+voisinage
    min_x=x-voisinage/2
    max_x=x+voisinage/2
    hauteur=1
    gauche=1
    droite=1
    for i in range(min_x,max_x):
        if img.getpixel((i, max_y)) == 0:
            hauteur=0
            break
    for i in range(min_y,max_y):
        if img.getpixel((min_x, i)) == 0:
            gauche=0
            break
        
    for i in range(min_y,max_y):
        if img.getpixel((max_x, i)) == 0:
            droite=0
            break
    
    return gauche,droite,hauteur



##################################################
##                  Variables                    #
##################################################

min_x = 0
min_y = 0
max_x = 0
max_y = 0
voisinage=10
##################################################
##                   Principal                   #
##################################################
img = Image.open('sample.png') # The image file must exist in the same directory as the script
img=img.convert('LA')
width, height = img.size
M=np.zeros((width,height),dtype=np.uint8)

numero_charactere=0
for i in range(width):
    for j in range(height):
        if img.getpixel((i,j))[0] < 100:
            a,b=i,j
            if M[i,j-1]!=0: M[i,j]=M[i,j-1]
            elif M[i-1,j-1]!=0: M[i,j]=M[i-1,j-1]
            elif M[i-1,j]!=0: M[i,j]=M[i-1,j]
            else:
                numero_charactere+=1
                M[i,j]=int(numero_charactere)

caractere_double=[] #deux tags sont equivalents

for i in range(1,width-1):
    for j in range(1,height-1):
        if M[i,j]!=0:
            a=M[i,j]
            if M[i,j-1]!=0 and M[i,j-1]!=a and [min(a,M[i,j-1]),max(a,M[i,j-1])] not in caractere_double:
                caractere_double.append([min(a,M[i,j-1]),max(a,M[i,j-1])])
            elif M[i-1,j-1]!=0 and M[i-1,j-1]!=a and[min(a,M[i-1,j-1]),max(a,M[i-1,j-1])] not in caractere_double:
                caractere_double.append([min(a,M[i-1,j-1]),max(a,M[i-1,j-1])])
            elif M[i-1,j]!=0 and M[i-1,j]!=a and[min(a,M[i-1,j]),max(a,M[i-1,j])] not in caractere_double:
                caractere_double.append([min(a,M[i-1,j]),max(a,M[i-1,j])])


