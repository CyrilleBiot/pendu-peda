#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Jeu du pendu
    Par Cyrille Biot
    Jeu du pendu, version pédagogique
    La moulinette du pendu est reprise du code de
    Didier Müller, http://www.nymphomath.ch/faq.html
    Sous licence contrat Creative Commons. (cf FAQ de son site)
    Modifié et adpaté par Cyrille BIOT.
"""
__author__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__license__ = "GPL"
__version__ = "1.0.6"
__date__ = "2020/02/20"
__maintainer__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"

import os, shutil
from random import choice
from operator import itemgetter
import unicodedata
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Copie des fichiers de conf dans le /home/ de l'user
# afin que celui ci puisse en rajouter
# La configuration est stockée dans /home/$user/.primtux/pendu-peda/data-files/
user = os.environ["USER"]
repertoire = '/home/' + user + '/.primtux/pendu-peda'
if not os.path.exists(repertoire):
    print("Le repertoire n'existe pas. On le créer")
    shutil.copytree('/usr/share/pendu-peda/data-files/', '/home/' + user + '/.primtux/pendu-peda/data-files/' )
else:
    print("Le repertoire existe. Configuration OK.")


# Initialisation des variables globales
score = 0
essai = 0
repData = '/home/' + user + '/.primtux/pendu-peda/data-files'
file = 'autre-liste-francais.txt'
sujet = 'Général'



def definirFichier(repData, file, sujet):
    fichier = open(str(repData) + '/' + str(file), "r")
    liste_mots = fichier.readlines()
    del liste_mots[0:3] # Nettoyage de l'entete
    fichier.close()
    change()
    changeTheme(file, sujet)
    return liste_mots

def creerMatrice():
    global repData
    matrice = []
    matriceCM = []
    matriceCE = []
    matriceAUTRE = []

    # Recuperation des entetes
    for fichiers in os.listdir(repData):
        with open(str(repData) + '/' + str(fichiers)) as f :
            listing = []
            for i in range(3):
                listing.append(f.readline().strip())
            listing.append(fichiers)
            matrice.append(listing)

    # Creation de 3 listes (une par niveau)
    for i in matrice:
        if 'CM' in (i[0]):
            matriceCM.append(i)
        elif 'CE' in i[0]:
            matriceCE.append(i)
        elif 'AUTRE' in i[0]:
            matriceAUTRE.append(i)
    # Tri de ces listes
    matriceCM = sorted(matriceCM, key=itemgetter(1))
    matriceCE = sorted(matriceCE, key=itemgetter(1))
    matriceAUTRE = sorted(matriceAUTRE, key=itemgetter(1))
    return matriceCM, matriceCE, matriceAUTRE, file

def lettre_dans_mot(lettre, bouton):
    global partie_en_cours, mot_partiel, mot_choisi, nb_echecs, image_pendu, score, essai
    if partie_en_cours:
        print("bouton",bouton)
        bouton.configure(state="disabled") # Desactive le bouton si cliqué
        nouveau_mot_partiel = ""
        lettre_dans_mot = False
        i = 0
        while i < len(mot_choisi):
            if mot_choisi[i] == lettre:
                nouveau_mot_partiel = nouveau_mot_partiel + lettre
                lettre_dans_mot = True
            else:
                nouveau_mot_partiel = nouveau_mot_partiel + mot_partiel[i]
            i += 1
        mot_partiel = nouveau_mot_partiel
        afficher_mot(mot_partiel)
        if not lettre_dans_mot:  # lettre fausse. Changer le dessin.
            nb_echecs += 1
            nomFichier = "images/pendu_" + str(nb_echecs) + ".gif"
            photo = PhotoImage(file=nomFichier)
            image_pendu.config(image=photo)
            image_pendu.image = photo
            if nb_echecs == 7:  # trop d'erreurs. Fini.
                partie_en_cours = False
                afficher_mot(mot_choisi)
                essai += 1
        elif mot_partiel == mot_choisi:
            partie_en_cours = False
            print("Vous avez gagné !")
            nomFichier = "images/pendu_10.gif"
            photo = PhotoImage(file=nomFichier)
            image_pendu.config(image=photo)
            image_pendu.image = photo
            score += 1
            essai += 1
            #return file

def afficher_mot(mot):
    global lettres, essai
    mot_large = ""
    i = 0
    while i < len(mot):  # ajoute un espace entre les lettres
        mot_large = mot_large + mot[i] + " "
        i += 1
    canevas.delete(lettres)
    lettres = canevas.create_text(320, 60, text=mot_large, fill='black', font='Courrier 30')

def afficherScore():
    global score, essai
    messageScore = "Partie(s) gagnée(s) : " + str(score)  + " sur " + str(essai) + "."
    #print(score, essai)
    return messageScore

def change():
    texte.configure(text=afficherScore())

def afficherTheme(file,sujet):
    return file, sujet

def changeTheme(file, sujet):
    file, sujet = afficherTheme(file, sujet)
    theme.configure(text=sujet)
    fileZone.configure(text=file)

def recupFile():
    # Nouvelle partie associée au bouton REJOUER
    f = fileZone.cget('text')
    t = theme.cget('text')
    for i in range(26): # On remet les boutons en actif
        bouton[i].configure(state="normal")
    init_jeu(f,t)


def init_jeu(file, sujet):
    global mot_choisi, mot_partiel, image_pendu, lettres, repData
    global nb_echecs, partie_en_cours, liste_mots
    nb_echecs = 0
    partie_en_cours = True
    liste_mots = definirFichier(repData, file, sujet)
    mot_choisi = choice(liste_mots).rstrip()
    mot_choisi = mot_choisi.upper()
    mot_choisi= ''.join((c for c in unicodedata.normalize('NFD', mot_choisi) if unicodedata.category(c) != 'Mn'))
    mot_partiel = "-" * len(mot_choisi)
    afficher_mot(mot_partiel)
    photo = PhotoImage(file="images/pendu_0.gif")
    image_pendu.config(image=photo)
    image_pendu.image = photo
    afficherScore()
    afficherTheme(file, sujet)
    print("mot:",mot_choisi)
    return file

# ======================================================================
# INTERFACE GRAPHIQUE
# ======================================================================

root = tk.Tk()
root.title("Le jeu du pendu")

style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="wn")


# Création des onglets
notebook = ttk.Notebook(root, style="top.TNotebook")
f1 = tk.Frame(notebook, bg="white", width=300, height=200)
f2 = tk.Frame(notebook, bg="blue", width=300, height=200)
f3 = tk.Frame(notebook, bg="yellow", width=300, height=200)
notebook.add(f1, text="Le Pendu pédagogique")
notebook.add(f2, text="Sélection des thèmes")
notebook.add(f3, text="A propos", sticky="NW")
notebook.grid(row=0, column=0, sticky="NW")

# ONGLET 1 : LE JEU
piedPage = Label(f1)
piedPage.pack(side=BOTTOM)
texte = Label(piedPage, text="Texte")
texte.grid(row=1,column=1)
theme = Label(piedPage, text="Texte")
theme.grid(row=1,column=2)
fileZone = Label(piedPage, text="Texte")
fileZone.grid(row=1,column=3)

canevas = Canvas(f1, bg='white', height=500, width=620)
canevas.pack(side=BOTTOM)
bouton = [0] * 26
for i in range(26):
    bouton[i] = ttk.Button(f1, text=chr(i + 65), width=2, state='normal'
                           , command=lambda x=i + 65, y=i: lettre_dans_mot(chr(x), bouton[y]))
    bouton[i].pack(side=LEFT)

photo = PhotoImage(file="images/pendu_0.gif")
image_pendu = Label(canevas, image=photo, border=0)
image_pendu.place(x=120, y=140)
lettres = canevas.create_text(320, 60, text="", fill='black', font='Courrier 30')

# ONGLET 2 : Les options
# Parse et recup data du dossier de config
matriceCM, matriceCE, matriceAUTRE, file = creerMatrice()
textMatriceCM = [0] * int(len(matriceCM))
boutonMatriceCM = [0] * int(len(matriceCM))
textMatriceCE = [0] * int(len(matriceCE))
boutonMatriceCE = [0] * int(len(matriceCE))
textMatriceAUTRE = [0] * int(len(matriceAUTRE))
boutonMatriceAUTRE = [0] * int(len(matriceAUTRE))

# Colonne CM
textCM = ttk.Label(f2, text="Niveaux CM", width=35, font='Courrier 10')
textCM.grid(row=0,column=1, sticky=W)
zone = tk.Frame(f2, padx=2, pady=2, height=2, width=200, bd=1, relief=SUNKEN)
a = 1
for i in range(len(matriceCM)):
    textMatriceCM[i] = ttk.Label(zone, text=matriceCM[i][2], width=35, font='Courrier 8')
    textMatriceCM[i].grid(row=a, column=0,sticky=W)
    boutonMatriceCM[i] = ttk.Button(zone, text="ok", width=2 , command=lambda x=matriceCM[i][3], y=matriceCM[i][2] : init_jeu(x,y))
    boutonMatriceCM[i].grid(row=a, column=1, sticky=W)
    a += 1
zone.grid(row=1,column=1,sticky=E)

# Colonne CE
textCE = ttk.Label(f2, text="Niveaux CE", width=35, font='Courrier 10')
textCE.grid(row=0, column=2, sticky=NW)
zone1 = tk.Frame(f2, padx=2, pady=2, height=2, width=200, bd=1, relief=SUNKEN)
a = 1
for i in range(len(matriceCE)):
    textMatriceCE[i] = ttk.Label(zone1, text=matriceCE[i][2], width=35, font='Courrier 8')
    textMatriceCE[i].grid(row=a, column=0, sticky=W)
    boutonMatriceCE[i] = ttk.Button(zone1, text="ok", width=2, command=lambda x=matriceCE[i][3], y=matriceCE[i][2] : init_jeu(x,y))
    boutonMatriceCE[i].grid(row=a,column=1, sticky=W)
    a += 1
zone1.grid(row=1,column=2,sticky=NW)

# Colonne de gauche
textAUTRE = ttk.Label(f2, text="Autres", width=35, font='Courrier 10')
textAUTRE.grid(row=0, column=3, sticky=NW)
zone2 = tk.Frame(f2, padx=2, pady=2, height=2, width=200, bd=1, relief=SUNKEN)
a = 1
for i in range(len(matriceAUTRE)):
    textMatriceAUTRE[i] = ttk.Label(zone2, text=matriceAUTRE[i][2], width=35, font='Courrier 8')
    textMatriceAUTRE[i].grid(row=a, column=0, sticky=W)
    boutonMatriceAUTRE[i] = ttk.Button(zone2, text="ok", width=2, command=lambda x=matriceAUTRE[i][3], y=matriceAUTRE[i][2] : init_jeu(x,y))
    boutonMatriceAUTRE[i].grid(row=a,column=1, sticky=W)
    a += 1
zone2.grid(row=1,column=3,sticky=NW)

# ONLET 3 : Configuration
message = __doc__ + '\n'
message += ('- - ' * 10) + '\n'
message += "Auteur(s) : " + __author__ + '\n'
message += ('- - ' * 10) + '\n'
message += "Copyright : " + __copyright__ + '\n'
message += ('- - ' * 10) + '\n'
message += "Crédits : " + __credits__ + '\n'
message += "Licence : " + __license__ + '\n'
message += "Version : " + __version__ + '\n'
message += "Date : " + __date__ + '\n'
message += "Mainteneur : " + __maintainer__ + '\n'
message += "Mail : " + __email__ + '\n'
message += "Status : " + __status__ + '\n'
message += ('- - ' * 10) + '\n'
message += 'Adapter votre configuration en ajoutant vos fichiers dans ce répertoire : ' + '\n'
message += repertoire + '/\n'

labelApropos = tk.Label(f3 , text=message, font='Courrier 10', justify='left')
labelApropos.pack(side=TOP)

# Bouton OK / QUITTER
bouton2 = ttk.Button(f1, text='Quitter', command=root.quit)
bouton2.pack(side=RIGHT)
bouton1 = ttk.Button(f1, text='Rejouer', command=recupFile)
bouton1.pack(side=RIGHT)

# ======================================================================
# Lancement Application
# ======================================================================
file = init_jeu(file,sujet)
root.mainloop()
root.destroy()