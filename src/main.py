"""
22 mars 2024, Copyright MUNAITPASOV Maksat
Universite Gustave Eiffel

pylint src/main.py
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
"""

import os
import csv
import subprocess


def extraire_nom_etudiant(nom_fichier):
    """
    Extrait le prenom et le nom de l'etudiant a partir du nom du fichier.

    Args:
        nom_fichier (str): Le nom du fichier contenant le prenom et le nom de l'etudiant.

    Returns:
        tuple: Un tuple contenant le prenom et le nom de l'etudiant.
    """
    nom_fichier_sans_extension = os.path.splitext(nom_fichier)[0]
    prenom, nom = nom_fichier_sans_extension.split('_')
    return prenom.capitalize(), nom.capitalize()



def compiler_fichier_c(chemin_fichier):
    """
    Compile un fichier C avec gcc en utilisant subprocess.

    Args:
        chemin_fichier (str): Le chemin absolu vers le fichier C a compiler.

    Returns:
        bool: True si la compilation reussie, False sinon.
    """
    nom_fichier_sans_extension = os.path.splitext(chemin_fichier)[0]
    fichier_compilable = nom_fichier_sans_extension + ".out"

    # Compiler le fichier avec gcc
    resultat_compilation = subprocess.run(\
        ["gcc", "-Wall", "-ansi", chemin_fichier, "-o", fichier_compilable],\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Verifier si la compilation a reussi
    if resultat_compilation.returncode == 0 and os.path.exists(fichier_compilable):
        return True, fichier_compilable, \
            len(resultat_compilation.stderr.decode().split('\n')) - 1

    return False, None, len(resultat_compilation.stderr.decode().split('\n')) - 1



def lancer_tests(fichier_compilable):
    """
    Lance les tests sur un fichier compile.

    Args:
        fichier_compilable (str): Le chemin absolu vers le fichier executable a tester.

    Returns:
        int: Le nombre de tests reussis.
    """
    tests = [
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1],
        [12, 12],
        [12, -43],
        [-1, -52]
    ]
    nb_tests_reussis = 0
    #reference_compilable = "reference.out"
    #subprocess.run(["gcc", "-Wall", "-ansi", "reference.c", "-o", reference_compilable])
    for test in tests:
        resultat_attendu = test[0] + test[1]

        resultat_test = subprocess.run( \
            ["./" + fichier_compilable, str(test[0]), str(test[1])], \
            stdout=subprocess.PIPE).stdout.decode().strip()

        if int(resultat_test.split()[-1]) == int(resultat_attendu):
            nb_tests_reussis += 1
    #os.remove(reference_compilable)
    return nb_tests_reussis



def compter_lignes_documentation(chemin_fichier):
    """
    Compte le nombre de lignes de documentation dans un fichier.

    Args:
        chemin_fichier (str): Le chemin absolu vers le fichier a analyser.

    Returns:
        int: Le nombre de lignes de documentation.
    """
    # Ouvrir le fichier et compter les lignes de documentation
    with open(chemin_fichier, 'r') as file:
        lignes = file.readlines()
        nb_lignes_doc = sum(1 for ligne in lignes if "/*" in ligne)
        return nb_lignes_doc


def generer_fichier_csv(chemin_dossier_etudiants):
    """
    Genere un fichier CSV contenant les informations relatives a chaque etudiant.

    Args:
        chemin_dossier_etudiants (str):
            Le chemin absolu vers le dossier contenant les fichiers des etudiants.
    """
    # Creation du fichier CSV
    with open('informations_etudiants.csv', 'w', newline='') as csvfile:
        fieldnames = ['Prenom', 'Nom', 'Compilation', 'Warnings',\
                        'Tests Reussis', 'Note de Qualite',\
                        'Note de Compilation', 'Note Finale']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Recuperer la liste des fichiers des etudiants

        for fichier in os.listdir(chemin_dossier_etudiants):
            if fichier.endswith(".c"):
                chemin_fichier = os.path.join(chemin_dossier_etudiants, fichier)

                # Informations sur l'etudiant
                prenom, nom = extraire_nom_etudiant(fichier)

                # Informations sur la compilation
                compilation_reussie, fichier_compilable, nb_warnings =\
                    compiler_fichier_c(chemin_fichier)

                # Nombre de tests reussis
                nb_tests_reussis = lancer_tests(fichier_compilable)\
                    if compilation_reussie else 0

                note_tests = nb_tests_reussis * (5/7) if not nb_tests_reussis else 0

                # Nombre de lignes de documentation
                nb_lignes_doc = compter_lignes_documentation(chemin_fichier)

                note_doc = nb_lignes_doc * (2/3) if nb_lignes_doc < 4 else 2

                note_compilation = ((compilation_reussie * 3) - (nb_warnings * 0.5))\
                    if (((compilation_reussie * 3) - (nb_warnings * 0.5)) > 0) else 0

                note_finale = note_compilation + note_tests + note_doc

                # ecrire les informations dans le fichier CSV
                writer.writerow({'Prenom': prenom, 'Nom': nom, \
                    'Compilation': int(compilation_reussie), 'Warnings': nb_warnings,\
                    'Tests Reussis': nb_tests_reussis, 'Note de Qualite': note_doc,
                    'Note de Compilation' : note_compilation, 'Note Finale': note_finale})


def nettoyer_executables(chemin_dossier_etudiants):
    """
    Nettoie tous les fichiers executables (.out) du repertoire des etudiants.

    Args:
        chemin_dossier_etudiants (str):
        Le chemin absolu vers le dossier contenant les fichiers des etudiants.
    """
    # Recuperer la liste des fichiers des etudiants
    liste_fichiers_etudiants = os.listdir(chemin_dossier_etudiants)

    # Supprimer tous les fichiers executables (.out)
    for fichier in liste_fichiers_etudiants:
        if fichier.endswith(".out"):
            chemin_fichier = os.path.join(chemin_dossier_etudiants, fichier)
            os.remove(chemin_fichier)



def main():
    """
    Le main de notre programme principale
    """
    chemin_dossier_etudiants = "eleves_bis"
    generer_fichier_csv(chemin_dossier_etudiants)

    nettoyer_executables(chemin_dossier_etudiants)



if __name__ == '__main__':
    main()
