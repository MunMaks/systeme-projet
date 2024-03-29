# Systeme mini-projet
## TP 8 : Mini projet de système

### Utilisation
Vous pouvez télécharger le répertoire d'après:<br>
`git clone https://github.com/MunMaks/systeme-projet`
et lancer avec la commande <b><i>python3 src/main.py</i></b>
Autrement dit, vous devez avoir `python3` déjà installé.


### Les fonctions principales

Au début j'ai fait plusieurs fonctions pour:
- Compiler les fichiers des étudiants
- Compter le nombre de lignes de documentation
- Extraire le nom et le prenom de l'étudiant
- Nettoyer tous les fichiers executables
- Lancer tests
- Generer le fichier csv 

Mais avant de faire les fonctions je décidé de passer 30 minutes en lisant tout le document pour comprendre la logique des tests, de l'évaluation et comment il faut documenter le code.
<br>

Après avoir compris l'idée principale j'ai décidé de commencer à écrire toutes les fonctions.
<br>

On peut commencer de la fonction `compter_lignes_documentation()`, cette fonction prend un string <b>chemin_fichier</b>. Après elle ouvre le fichier en mode lécture et ligne par ligne recherche les commentaires en C de type: "/*" ou "//"
<br>

Traitons la fonction `extraire_nom_etudiant()`, cette fonction prend un string <b>nom_fichier</b>.
Elle effectue l'extraction de nom et de prénom de l'étudiant de son fichier nomée  prenom_nom.c.
<br>

Ensuite, il y a une autre fonction intéressante, c'est `compiler_fichier_c()`, cette fonction prend un string <b>chemin_fichier</b>.
D'abord on obtient le nom du fichier sans extension et on crée le fichier compilable pour pouvoir le compiler grâce à subprocess.run et utilisant <b>gcc</b> et les flags comme  <b>-Wall -ansi</b>.
On vérifie aussi si la compilation a bien passé et que le fichier exécutable existe alors, on renvoie un tuple qui contient 3 éléments:
- Un booleen indiquant si la compilation a reussi.
- Le chemin absolu vers le fichier compile (si la compilation a reussi).
- Le nombre de warnings emis par le compilateur lors de la compilation.
<br>

De plus, nous avons la fonction `lancer_tests()` cette fonction prend un string <b>fichier_executable</b>.
Elle contient des tests et elle renvoie le nombre de tests réussis par le fichier de l'étudiant.
<br>

Il nous reste à traiter quelques fonctions, comme `nettoyer_executables()` qui ne prend aucun paramètre et ne renvoie rien.
Cette fonction va nettoyer tous les fichiers executables qu'on a produit pendant la compilation des fichier des étudiants.
Nous avons appelé les fichier exécutable par <b>prenom_nom.out</b>, donc il suffit de parcourir toute les fichiers des étudiants y compris .c et .out et si on voit le fichier.out on appele la système <b>os</b> et on détruit ces fichiers.
J'utilise aussi try, except pour être sûr que la suppression a bien passé, sinon j'affiche le message d'erreur.
`https://docs.python.org/3/library/exceptions.html#OSError`
<br>

Il existe aussi la fonction `calculs()` cette fonction prend un string <b>fichier</b>.
Elle fait l'appel de chaque fonction précédente afin de calculer la note finale de chaque étudiant à partir de son fichier.c
<br>

Enfin, la dernière fonction dans mon class `GestionEtudiants()` qui ne prend rien et ne renvoie rien.
Cette une grande fonction et au même temps très importante, car elle effectue la création de notre fichier.csv souhaité.
On commence par la création de `informations_etudiants.csv` en mode écriture, qui crée les colonnes comme:
- Prenom
- Nom
- Compilation
- Warnings
- Tests Reussis
- Note de Qualite
- Note de Compilation
- Note Finale

<br>

Et pour chaque étudiant on fait les calculs, d'après la fonction précédente `calculs()` et ensuite on va insérer des étudiants l'un après l'autre avec leurs résultats.
<br>

Après d'après les bonnes habitudes on doit aussi créer la fonction `main()` qui va exécuter notre code et pour finir la constructino vitale c'est:
```
if __name__ == '__main__':
    main()
```

## Conclusion
C'était un bon projet pour comprendre comment travailler avec os, subprocess, fichiers .csv et surtout la compréhension profonde de Python3.

## Author
- MUNAITPASOV Maksat
