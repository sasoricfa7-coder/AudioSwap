# This file is part of AudioSwap.
# Copyright (C) 2026 Sasori
# Licensed under the GNU AGPLv3-or-later. See the LICENSE file
# at the project root.

import subprocess as sub
import sys
from pathlib import Path
import os

_audio = "audio"
_video = "video" # En utilisant de variables global adapter le script deviens facile
EXTENSIONS_VIDEO = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}

def arret() :
    sys.exit(1)

def nom_base_1() :
    nom = input("Entrez le nom de base : ").strip()
    compteur = 0
    while nom == "" :
        nom = input("Entrez un nom correct : ").strip()
        compteur += 1 # On va perdre notre temps s'il ne sais pas choisir on vba l'aider
        if compteur == 3 :
            nom = "output"
    return nom

def _FFmpeg() : # Je les ai separer pour que tout soit claire pour moi et pouvoir sire exactement à l'utilisateur ou ca va pas
    try :
        sub.run(["ffmpeg", "-version"])
    except Exception as e :
        print("outils de base manquant.")
        print("Veuillez installer ffmpeg")
        arret()

def _FFprobe() :
    try :
        sub.run(["ffprobe", "-version"])
    except Exception as e :
        print("outils de base manquant.")
        print("Veuillez installer ffprobe")
        arret()

def verification_dossier() :
    global _audio, _video

    if not os.path.isdir(_audio) :
        print("Le dossier pour utiliser les audio n'existe pas.")
        print("S'il existe veuillez le renommer : audio")
        arret()
    if not os.path.isdir(_video) :
        print("Le dossier pour utiliser les video n'existe pas.")
        print("S'il existe veuillez le renommer : video")
        arret()

def verification_contenu() :
    global EXTENSIONS_VIDEO, _audio, _video

    contenu_audio = Path(_audio)
    if not any(contenu_audio.iterdir()) :
        print("Dossier audio vide.")
        arret()

    liste_audio = []
    for f in contenu_audio.iterdir() :
        if f.is_file() and f.suffix.lower() in EXTENSIONS_VIDEO :
            liste_audio.append(f)
        else :
            print("Le dossier audio contient des fichiers non supporter")
            print("Extension supporter ", EXTENSIONS_VIDEO)
            arret()

    contenu_video = Path(_video)
    if not any(contenu_video.iterdir()) :
        print("Dossier video vide.")
        arret()

    liste_video = []
    for f in contenu_video.iterdir() :
        if f.is_file() and f.suffix.lower() in EXTENSIONS_VIDEO :
            liste_video.append(f)
        else :
            print("Le dossier video contient des fichiers non supporter")
            print("Extension supporter ", EXTENSIONS_VIDEO)
            arret()

    if len(liste_video) != len(liste_audio) :
        print("Chaque dossier doivent avoir exactement le même nombre de fichier")
        print(f"Dossier audio : {len(liste_audio)} fichiers. or Dossier video : {len(liste_video)} fichiers")
        arret()

def verification_preliminaire() :
    _FFmpeg()
    print("\n")
    _FFprobe()
    print("\n")
    verification_dossier()
    print("\n")
    verification_contenu()
    print("\n")

def main() : # une petite règle : chaque fonction gère ses erreurs
    nom = nom_base_1()
    verification_preliminaire()



    print("Succès") # Pour le guider et savoir que tout a marcher

if __name__=="__main__" :
    main()
