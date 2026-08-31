📖 Description
AudioSwap est un script Python qui permet de remplacer la piste audio d'un fichier vidéo par la piste audio d'un autre fichier vidéo.

Cas d'usage typique : Vous avez un épisode d'anime japonais avec des sous-titres français incrustés, mais vous préférez la piste audio anglaise. Vous possédez également le même épisode en anglais. AudioSwap va prendre la vidéo (avec les sous-titres) de la version japonaise et l'audio de la version anglaise, et les assembler en un seul fichier.

🎯 Objectif
Cet outil est conçu pour les apprenants en langues qui souhaitent regarder du contenu avec :

L'audio dans la langue cible (ex : anglais)

Les sous-titres dans leur langue natale (ex : français)

En combinant le meilleur des deux versions, vous obtenez une expérience d'apprentissage optimale.

✨ Fonctionnalités
✅ Traitement par lot – Traite plusieurs fichiers en une seule fois

✅ Validation stricte – Tout est vérifié avant le moindre traitement

✅ Vérification des durées – S'assure que les durées audio/vidéo correspondent exactement (tolérance 0)

✅ Flexibilité des extensions – Supporte les formats vidéo mixtes (.mp4, .mkv, .avi, .mov, .webm)

✅ Sortie automatique – Crée un dossier produits_finaux/ avec des fichiers numérotés

✅ Gestion des conflits – Ajoute automatiquement des suffixes si les fichiers existent déjà

✅ Messages d'erreur clairs – Des détails précis pour chaque problème rencontré

✅ README bilingue – Documentation disponible en anglais et en français

🧰 Prérequis
Python 3.6+

FFmpeg (avec ffprobe) – installé et accessible dans votre PATH

Installation de FFmpeg
OS	Commande / Instructions
Ubuntu/Debian	sudo apt install ffmpeg
macOS (Homebrew)	brew install ffmpeg
Windows	Télécharger sur ffmpeg.org et ajouter au PATH
Vérifier l'installation :

bash
ffmpeg -version
ffprobe -version
📁 Structure du projet
text
AudioSwap/
├── video/              ← Vidéos sources avec sous-titres (on garde la vidéo)
├── audio/              ← Vidéos sources avec l'audio désiré (on garde l'audio)
├── produits_finaux/    ← Dossier de sortie (créé automatiquement)
└── audioswap.py        ← Script principal
🚀 Utilisation
1. Préparez vos fichiers
Placez vos fichiers vidéo dans les dossiers appropriés :

Dossier	Contenu	Ce qui est conservé
video/	Vidéos avec les sous-titres souhaités (ex : version japonaise)	Piste vidéo uniquement
audio/	Vidéos avec l'audio souhaité (ex : version anglaise)	Piste audio uniquement
Important : Les deux dossiers doivent contenir le même nombre de fichiers, et les fichiers sont appariés par ordre alphabétique.

2. Lancez le script
bash
python audioswap.py
3. Suivez les instructions
text
Entrez le nom de base pour les fichiers de sortie : MonAnime
4. Validation
Le script effectue une vérification complète avant tout traitement :

FFmpeg/ffprobe sont installés

Les deux dossiers existent

Chaque dossier contient au moins un fichier vidéo valide

Le nombre de fichiers dans les deux dossiers est égal

Toutes les durées vidéo correspondent exactement (paire par paire)

Le dossier de sortie peut être créé/écrit

Si une seule vérification échoue, le script s'arrête immédiatement avec un message d'erreur clair.

5. Résultat
Les fichiers sont générés sous la forme :

text
produits_finaux/[nom_base]_01.mp4
produits_finaux/[nom_base]_02.mp4
...
Si un fichier existe déjà, un suffixe est ajouté automatiquement :

text
produits_finaux/[nom_base]_01_1.mp4
🔧 Détails techniques
Fonctionnement
Phase de validation : Tous les prérequis et paires de fichiers sont vérifiés

Phase de traitement : Pour chaque paire valide :

Extraire le flux vidéo du fichier dans video/

Extraire le flux audio du fichier dans audio/

Les assembler en un seul fichier .mp4 via FFmpeg

Commande FFmpeg utilisée
Le script utilise cette commande FFmpeg (conceptuellement) :

bash
ffmpeg -i video_source.mp4 -i audio_source.mp4 \
       -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
-c:v copy – Copie le flux vidéo sans ré-encodage (rapide)

-map 0:v:0 – Prend la première piste vidéo de la première entrée

-map 1:a:0 – Prend la première piste audio de la seconde entrée

-shortest – Coupe à la durée la plus courte (mesure de sécurité)

Extensions vidéo supportées
.mp4

.mkv

.avi

.mov

.webm

(Vous pouvez modifier la liste dans le script si nécessaire)

⚠️ Gestion des erreurs
Le script effectue une pré-validation stricte. Si l'un de ces problèmes est détecté, il s'arrête immédiatement :

Problème	Message
FFmpeg non installé	❌ ERREUR : FFmpeg n'est pas installé ou inaccessible.
Dossier manquant	❌ ERREUR : Le dossier "video/" est introuvable.
Dossier vide	❌ ERREUR : Le dossier "video/" est vide.
Fichier non supporté	❌ ERREUR : "video/image.jpg" n'est pas un fichier vidéo supporté.
Comptes différents	❌ ERREUR : video/ contient 5 fichiers, audio/ contient 3 fichiers.
Durées différentes	❌ ERREUR : Durées différentes : ep03.mp4 (23.456s) ≠ ep03_EN.mp4 (24.123s).
Droits d'écriture	❌ ERREUR : Impossible de créer/écrire dans "produits_finaux/".
📄 Licence
Ce projet est sous licence GNU Affero General Public License v3.0 ou ultérieure (AGPL-3.0-or-later).

Cette licence garantit que :

Le code source reste ouvert

Les modifications doivent être partagées

L'utilisation en réseau est considérée comme une distribution

Voir le fichier LICENSE pour plus de détails.

🤝 Contributions
Les contributions sont les bienvenues ! Ouvrez une issue ou soumettez une pull request.

Directives
Forkez le dépôt

Créez une branche de fonctionnalité

Faites vos modifications

Soumettez une pull request avec une description claire

📧 Contact
Pour toute question, suggestion ou problème, ouvrez une issue GitHub.

🌟 Remerciements
FFmpeg – Le framework multimédia qui rend tout cela possible

