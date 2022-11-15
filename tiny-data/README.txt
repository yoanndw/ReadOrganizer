## Jeu de données "tiny-data" du projet BIF 2022-2023

Ce répertoire contient :
* ref_genome.fasta : 1 génome de 1000 pb (format fasta : 1ere ligne = nom de la séquence précédée de '>' ; 2ème ligne = séquence ADN)
* reads.fasta : 11 lectures de taille 100 simulées sur ce génome, au format fasta (2 lignes par lecture)
* reads.txt : ces mêmes 11 lectures au format txt (1 ligne par lecture, juste les séquences, sans les noms)

Le fichier reads.fasta n'est pas à donner en entrée de votre programme, mais il contient dans les noms de chaque lecture la "vraie" position où a été échantillonnée la lecture sur le génome : c'est-à-dire la position que doit renvoyer votre algorithme de mapping.

Ce jeu de donnée permet de tester l'exactitude de votre algorithme de mapping. Il ne permet pas d'évaluer le comportement de votre programme en termes de taux de compression, temps de calcul et empreinte mémoire.

 