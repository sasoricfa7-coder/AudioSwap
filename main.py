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
dossier_sortie = "produits_finaux"

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
            liste_audio.append(f.name)
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
            liste_video.append(f.name)
        else :
            print("Le dossier video contient des fichiers non supporter")
            print("Extension supporter ", EXTENSIONS_VIDEO)
            arret()
    liste_video = sorted(liste_video)
    liste_audio = sorted(liste_audio)
    
    if len(liste_video) != len(liste_audio) :
        print("Chaque dossier doivent avoir exactement le même nombre de fichier")
        print(f"Dossier audio : {len(liste_audio)} fichiers. or Dossier video : {len(liste_video)} fichiers")
        arret()

    for i in range(len(liste_audio)) :
        liste_audio[i] = _audio + "/" + liste_audio[i]

    for i in range(len(liste_video)) :
        liste_video[i] = _video + "/" + liste_video[i]

    return liste_audio, liste_video

def verification_preliminaire() :
    _FFmpeg()
    _FFprobe()
    verification_dossier()

    return verification_contenu()

def validation_etape1(liste_audio, liste_video) :
    print("✅ Toutes les vérifications sont passées.")
    print("\t- FFmpeg : OK")
    print("\t- FFprobe : OK")
    print("\t- Dossiers : OK")
    print(f"\t- Fichiers vidéo : video/ {len(liste_video)} audio/ {len(liste_audio)}")
    print("\t- Nombres : OK")
    print(f"Prêt à traiter {len(liste_video)} paire.")

def verification_duree(i, j) :
    try :
        resultat_audio = sub.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", i] , capture_output=True, text = True)
        resultat_video = sub.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", j] , capture_output=True, text = True)

        r_audio_str = resultat_audio.stdout.strip()
        d1 = float(r_audio_str)
        
        r_video_str = resultat_video.stdout.strip()
        d2 = float(r_video_str)


        if abs(d1 - d2) > 0.1 :
            print(f"La paire est incompatible : {i} --> {j}")
            arret()
        return d1, d2
    except Exception as e :
        print(f"Fichier potentiellement corrompu : {i} --> {j}")
        arret()

def traitement_duree(la, lv) :
    #ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 fichier.mp4
    paire = []
    for i , j in zip(la, lv) :
        d1, d2 = verification_duree(i, j)
        t = (i, j, d1, d2)
        paire.append(t)

    return paire

def creer_dossier_sortie() :
    global dossier_sortie
    dossier = Path(dossier_sortie)
    i = 0
    while dossier.exists() :
        nom = dossier_sortie + "_" + str(i)
        dossier = Path(nom)
        i += 1

    dossier.mkdir(exist_ok=True)
    return dossier

def construire_nom_sortie(nom_base, index, d) :
    nom =  f"{nom_base}_{index}.mp4"
    nom_complet = d.name + "/" + nom
    return Path(nom_complet)

def remplacer_audio(fichier_video, fichier_audio, fichier_sortie):
    """Remplace l'audio d'un fichier vidéo."""
    cmd = [
        "ffmpeg",
        "-i", fichier_video,
        "-i", fichier_audio,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-y",  # Écraser sans demander
        str(fichier_sortie)
    ]
    
    try:
        resultat = sub.run(cmd, capture_output=True, text=True)
        if resultat.returncode != 0:
            print(f"❌ Erreur FFmpeg : {resultat.stderr}")
            arret()

    except Exception as e:
        print(f"❌ Erreur : {e}")
        arret()

def traitement_audio(paires, n, d) : # i , j , d1, d2
    j = 0
    for i in paires :
        remplacer_audio( Path(i[1]), Path(i[0]), Path(construire_nom_sortie(n, j, d)))
        j += 1 
        
    print("Succès.")
    

def main() : # une petite règle : chaque fonction gère ses erreurs
    nom = nom_base_1()
    liste_audio, liste_video =  verification_preliminaire()
    validation_etape1(liste_audio, liste_video)

    liste_des_paires = traitement_duree(liste_audio, liste_video)
    dossier =  creer_dossier_sortie()
    print("Dossier créer : ", dossier.name)

    traitement_audio(liste_des_paires, nom, dossier)

if __name__=="__main__" :
    main()
