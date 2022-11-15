## Jeux de données "real-data" du projet BIF 2022-2023

Ce répertoire contient 2 types de fichiers :
* Les fichiers *.fasta sont les génomes de référence (format fasta : 1ere ligne = nom de la séquence précédée de '>' ; 2ème ligne = séquence ADN)
* Les fichiers *_reads_*x.txt.gz sont les fichiers de séquençage compressés par gzip. Format txt : chaque ligne contient la séquence d'une lecture de séquençage (taille 100).

Le génome 'humch1_100Kb.fasta' correspond aux 100 premiers Kb du chromosome 1 du génome humain (taille  = 100 000 bp). Sur ce génome, 6 fichiers de séquençage ont été générés, à 6 profondeurs de séquençage différentes : 5x, 10x, 20x, 40x, 80x, 120x. 
Par exemple : 'humch1_100Kb_reads_40x.txt' correspond au séquençage de 'humch1_100Kb.fasta' à 40x, il contient 40000 lectures de taille 100.

Le génome 'humch1_1Mb.fasta' correspond au premier 1Mb du chromosome 1 du génome humain (taille  = 1 000 000 bp). Sur ce génome, 1 seul fichier de séquençage a été généré, à 40x de profondeur de séquençage : 'humch1_1Mb_reads_40x.txt'.


Note : les données humch1_100Kb sont suffisantes pour effectuer vos tests. Les données sur 1Mb sont mises à disposition si vous voulez tester votre programme sur un jeu de données encore plus gros (et plus réaliste).


