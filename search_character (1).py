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



##################################################
##                  Variables                    #
##################################################


##################################################
##                   Principal                   #
##################################################
img = Image.open('sample.PNG') # The image file must exist in the same directory as the script
img=img.convert('LA')
width, height = img.size
M=np.zeros((width,height),dtype=np.uint8)

numero_charactere=0
for i in range(width):
    for j in range(height):
        if img.getpixel((i,j))[0] < 100:
            if M[i,j-1]!=0: M[i,j]=M[i,j-1]
            elif M[i-1,j-1]!=0: M[i,j]=M[i-1,j-1]
            elif M[i-1,j]!=0: M[i,j]=M[i-1,j]
            else:
                numero_charactere+=1
                M[i,j]=int(numero_charactere)

caractere_double=[]

for i in range(1,width-1):
    for j in range(1,height-1):
        if M[i,j]!=0:
            a=M[i,j]
            if M[i,j-1]!=0 and M[i,j-1]!=a and [min(a,M[i,j-1]),max(a,M[i,j-1])] not in caractere_double:
                caractere_double.append([min(a,M[i,j-1]),max(a,M[i,j-1])])
                
            elif M[i-1,j-1]!=0 and M[i-1,j-1]!=a and [min(a,M[i-1,j-1]),max(a,M[i-1,j-1])] not in caractere_double:
                caractere_double.append([min(a,M[i-1,j-1]),max(a,M[i-1,j-1])])
                
            elif M[i-1,j]!=0 and M[i-1,j]!=a and [min(a,M[i-1,j]),max(a,M[i-1,j])] not in caractere_double:
                caractere_double.append([min(a,M[i-1,j]),max(a,M[i-1,j])])

liste_caractere=[]
for x in caractere_double:
    Ok=1
    for y in liste_caractere:
        if x[0] in y:
            Ok=0
            if x[1] not in y:
                y.append(x[1])
                break
        elif x[1] in y:
            Ok=0
            if x[0] not in y:
                y.append(x[0])
                break
    if Ok:
        liste_caractere.append([x[0],x[1]])
    print(liste_caractere)
        

def f(j,y):  #sous fonction de g
    for i in range(0,len(caractere_double)):
        a=i
        x=caractere_double[a]
        if j in x:            
            if x[1] not in y:
                y.append(x[1])
            else:
                y.append(x[0])
            caractere_double.pop(i)
            break
            #len(caractere_double) est modifié, on sort de la boucle pour rappeler la fonction f avec "a" comme initialisation de la nouvelle boucle
    if a>=len(caractere_double)-1:
        #on est pas rentré dans le "if j in x", donc on a exploré la liste caractere_double en entier
        return 
    f(j,y,a)

def g(liste_caractere):
    y=caractere_double.pop(0)
    liste_caractere.append(y)
    for i in y:
        if len(caractere_double)==0:
            return
        f(i,y)
        #on cherche les couples ayant un membre égale à i dans la liste caractère_double, et on l'ajoute dans y
    #y n'est pas le dernier caractère, il en reste d'autres
    if len(caractere_double!=0):
        g(liste_caractere)
    
liste_caractere=[]

                  

       
               